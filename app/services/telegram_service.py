import asyncio
from io import BytesIO
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.error import TelegramError
from app.services.ai_service import get_gemini_response
from app.services.audio_service import transcribe_audio, text_to_speech, get_language_code
from app.models.bot import Bot as BotModel
from app.models.user_preference import UserPreference
from app import db


async def send_typing_action(bot: Bot, chat_id: int):
    """Send typing indicator to show bot is processing."""
    try:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    except TelegramError as e:
        print(f"Error sending typing action: {e}")


async def send_message(bot: Bot, chat_id: int, text: str):
    """Send a message via Telegram bot."""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        print(f"Error sending message: {e}")
        raise


async def send_voice_message(bot: Bot, chat_id: int, audio_bytes: bytes):
    """Send a voice/audio message via Telegram bot."""
    try:
        # Detect audio format from magic bytes
        if audio_bytes[:4] == b'RIFF':
            # WAV format
            filename = 'response.wav'
            mime_type = 'audio/wav'
        elif audio_bytes[:3] == b'ID3' or audio_bytes[:2] == b'\xff\xfb' or audio_bytes[:2] == b'\xff\xf3':
            # MP3 format
            filename = 'response.mp3'
            mime_type = 'audio/mpeg'
        elif audio_bytes[:4] == b'OggS':
            # OGG format
            filename = 'response.ogg'
            mime_type = 'audio/ogg'
        else:
            # Default to MP3
            filename = 'response.mp3'
            mime_type = 'audio/mpeg'
        
        audio_file = BytesIO(audio_bytes)
        audio_file.name = filename
        
        print(f"📤 Sending voice: {filename} ({len(audio_bytes)} bytes, mime: {mime_type})")
        
        # Use send_voice for voice messages (shows as voice note)
        await bot.send_voice(
            chat_id=chat_id,
            voice=audio_file
        )
        
        print(f"✅ Audio sent successfully!")
        
    except TelegramError as e:
        print(f"❌ Error sending audio: {e}")
        raise


async def process_telegram_message(bot_model: BotModel, message_text: str, chat_id: int, telegram_user_id: int = None):
    """
    Process incoming Telegram message and send AI response.
    
    Args:
        bot_model: The Bot database model
        message_text: User's message text
        chat_id: Telegram chat ID to send response to
        telegram_user_id: Telegram user ID for language preference
        
    Returns:
        dict: Response status
    """
    try:
        # Validate bot has at least one token
        tokens = bot_model.get_telegram_tokens()
        if not tokens:
            return {
                'success': False,
                'error': 'Bot does not have any Telegram tokens configured'
            }
        
        # Initialize Telegram Bots (one for each token)
        telegram_bots = [Bot(token=token) for token in tokens]
        # Use the first bot for now (can be improved to use all bots)
        telegram_bot = telegram_bots[0]
        
        # Check for /start or /language command
        if message_text.strip().lower() in ['/start', '/language', '/til', '/язык']:
            print(f"🌐 Language selection for chat {chat_id}")
            result = await send_language_selection(telegram_bot, chat_id)
            print(f"✅ Language menu sent: {result}")
            return {
                'success': True,
                'response': 'Language selection sent'
            }
        
        # Send typing indicator
        await send_typing_action(telegram_bot, chat_id)
        
        # Get user language preference
        user_language = bot_model.language  # Default to bot language
        if telegram_user_id:
            preference = get_or_create_user_preference(bot_model.id, telegram_user_id)
            user_language = preference.language
        
        # Get knowledge base if available
        from app.services.kb_service import combine_knowledge_bases
        knowledge_bases = bot_model.knowledge_bases.all()
        kb_text = combine_knowledge_bases(knowledge_bases) if knowledge_bases else None
        
        # Get AI response using user's language preference
        ai_response = get_gemini_response(
            user_message=message_text,
            system_prompt=bot_model.system_prompt,
            language=user_language,
            knowledge_base_text=kb_text
        )
        
        print(f"🤖 AI Response ({user_language}): {ai_response[:100]}...")
        
        # Send text response first
        await send_message(telegram_bot, chat_id, ai_response)
        
        # Generate and send audio response ALWAYS
        from app.services.audio_service import text_to_speech, get_language_code
        language_code = get_language_code(user_language)
        
        print(f"🔊 Generating audio response in {language_code}...")
        audio_bytes = text_to_speech(ai_response, language_code)
        
        if audio_bytes:
            await send_voice_message(telegram_bot, chat_id, audio_bytes)
            print(f"✅ Audio response sent!")
        else:
            print(f"⚠️ Audio generation failed")
        
        return {
            'success': True,
            'response': ai_response,
            'audio_sent': bool(audio_bytes)
        }
        
    except TelegramError as e:
        error_msg = f"Telegram API error: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'error': error_msg
        }


async def process_voice_message(bot_model: BotModel, voice_file_id: str, chat_id: int, telegram_user_id: int = None):
    """
    Process incoming Telegram voice message and send AI response with audio.
    
    Args:
        bot_model: The Bot database model
        voice_file_id: Telegram voice file ID
        chat_id: Telegram chat ID to send response to
        telegram_user_id: Telegram user ID for language preference
        
    Returns:
        dict: Response status
    """
    try:
        # Validate bot has at least one token
        tokens = bot_model.get_telegram_tokens()
        if not tokens:
            return {
                'success': False,
                'error': 'Bot does not have any Telegram tokens configured'
            }
        
        # Initialize Telegram Bots (one for each token)
        telegram_bots = [Bot(token=token) for token in tokens]
        # Use the first bot for now (can be improved to use all bots)
        telegram_bot = telegram_bots[0]
        
        # Send typing indicator
        await send_typing_action(telegram_bot, chat_id)
        
        # Download voice file
        voice_file = await telegram_bot.get_file(voice_file_id)
        voice_bytes = await voice_file.download_as_bytearray()
        
        # Get user language preference
        user_language = bot_model.language  # Default to bot language
        if telegram_user_id:
            preference = get_or_create_user_preference(bot_model.id, telegram_user_id)
            user_language = preference.language
        
        # Get language code
        language_code = get_language_code(user_language)
        
        # Transcribe audio to text using Google Speech Recognition
        print(f"🎤 Transcribing voice message...")
        transcribed_text = transcribe_audio(bytes(voice_bytes), language_code)
        print(f"📝 Transcribed: {transcribed_text}")
        
        # Check if transcription failed
        if 'iltimos' in transcribed_text.lower() or 'xatolik' in transcribed_text.lower():
            # Transcription failed, just send the error message
            await send_message(telegram_bot, chat_id, transcribed_text)
            return {
                'success': True,
                'transcription': '[Failed]',
                'response': transcribed_text,
                'voice_sent': False
            }
        
        # Get knowledge base if available
        from app.services.kb_service import combine_knowledge_bases
        knowledge_bases = bot_model.knowledge_bases.all()
        kb_text = combine_knowledge_bases(knowledge_bases) if knowledge_bases else None
        
        # Get AI response using user's language preference
        ai_response = get_gemini_response(
            user_message=transcribed_text,
            system_prompt=bot_model.system_prompt,
            language=user_language,
            knowledge_base_text=kb_text
        )
        
        print(f"🤖 AI Response: {ai_response[:100]}...")
        
        # Send text response first
        await send_message(telegram_bot, chat_id, ai_response)
        
        # Generate and send audio response
        print(f"🔊 Generating audio response...")
        audio_bytes = text_to_speech(ai_response, language_code)
        
        if audio_bytes:
            await send_voice_message(telegram_bot, chat_id, audio_bytes)
            print(f"✅ Audio response sent!")
        else:
            print(f"⚠️ Audio generation failed")
        
        return {
            'success': True,
            'transcription': transcribed_text,
            'response': ai_response,
            'voice_sent': bool(audio_bytes)
        }
        
    except TelegramError as e:
        error_msg = f"Telegram API error: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f"Error processing voice message: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': error_msg
        }


def run_async(coro):
    """
    Helper function to run async code from sync context.
    Creates new event loop if needed.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)


async def set_webhook(bot_token: str, webhook_url: str):
    """
    Set webhook URL for a Telegram bot.
    
    Args:
        bot_token: Telegram bot token
        webhook_url: Full webhook URL
        
    Returns:
        dict: Status of webhook setup
    """
    try:
        bot = Bot(token=bot_token)
        result = await bot.set_webhook(url=webhook_url)
        
        if result:
            webhook_info = await bot.get_webhook_info()
            return {
                'success': True,
                'webhook_url': webhook_info.url,
                'pending_update_count': webhook_info.pending_update_count
            }
        else:
            return {
                'success': False,
                'error': 'Failed to set webhook'
            }
            
    except TelegramError as e:
        return {
            'success': False,
            'error': f"Telegram error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error: {str(e)}"
        }


async def delete_webhook(bot_token: str):
    """
    Delete webhook for a Telegram bot.
    
    Args:
        bot_token: Telegram bot token
        
    Returns:
        dict: Status of webhook deletion
    """
    try:
        bot = Bot(token=bot_token)
        result = await bot.delete_webhook()
        
        return {
            'success': result,
            'message': 'Webhook deleted successfully' if result else 'Failed to delete webhook'
        }
        
    except TelegramError as e:
        return {
            'success': False,
            'error': f"Telegram error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error: {str(e)}"
        }


async def get_bot_info(bot_token: str):
    """
    Get information about a Telegram bot.
    
    Args:
        bot_token: Telegram bot token
        
    Returns:
        dict: Bot information
    """
    try:
        bot = Bot(token=bot_token)
        me = await bot.get_me()
        
        return {
            'success': True,
            'bot': {
                'id': me.id,
                'username': me.username,
                'first_name': me.first_name,
                'can_join_groups': me.can_join_groups,
                'can_read_all_group_messages': me.can_read_all_group_messages,
                'supports_inline_queries': me.supports_inline_queries
            }
        }
        
    except TelegramError as e:
        return {
            'success': False,
            'error': f"Invalid token or Telegram error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error: {str(e)}"
        }


def get_or_create_user_preference(bot_id: int, telegram_user_id: int) -> UserPreference:
    """Get or create user preference for a specific bot and user."""
    preference = UserPreference.query.filter_by(
        bot_id=bot_id,
        telegram_user_id=telegram_user_id
    ).first()
    
    if not preference:
        preference = UserPreference(
            bot_id=bot_id,
            telegram_user_id=telegram_user_id,
            language='uz'  # Default language
        )
        db.session.add(preference)
        db.session.commit()
    
    return preference


async def send_language_selection(bot: Bot, chat_id: int):
    """Send language selection menu to user."""
    try:
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            ],
            [
                InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message_text = (
            "Choose language / Выберите язык / Tilni tanlang / Elige idioma:\n\n"
            "Select your preferred language for bot responses."
        )
        
        await bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=reply_markup
        )
        
        return {'success': True}
        
    except TelegramError as e:
        print(f"Error sending language selection: {e}")
        return {'success': False, 'error': str(e)}


async def handle_language_callback(bot_model: BotModel, callback_query_data: dict, chat_id: int, message_id: int):
    """Handle language selection callback."""
    try:
        # Get bot tokens
        tokens = bot_model.get_telegram_tokens()
        if not tokens:
            return {'success': False, 'error': 'No telegram tokens configured'}
        
        telegram_bot = Bot(token=tokens[0])
        
        # Extract callback data
        callback_data = callback_query_data.get('data', '')
        telegram_user_id = callback_query_data.get('from', {}).get('id')
        
        if not telegram_user_id:
            return {'success': False, 'error': 'No user ID in callback'}
        
        if callback_data.startswith('lang_'):
            language = callback_data.split('_')[1]  # uz, ru, en
            
            # Save user preference
            preference = get_or_create_user_preference(bot_model.id, telegram_user_id)
            preference.language = language
            db.session.commit()
            
            # Language names
            lang_names = {
                'en': "English 🇬🇧",
                'ru': "Русский 🇷🇺",
                'uz': "O'zbekcha 🇺🇿",
                'es': "Español 🇪🇸"
            }
            
            # Confirmation messages
            confirmations = {
                'en': f"✅ Language changed to: {lang_names.get(language, language)}\n\nI will now respond in {lang_names.get(language)}.",
                'ru': f"✅ Язык изменен: {lang_names.get(language, language)}\n\nТеперь я буду отвечать на {lang_names.get(language)}.",
                'uz': f"✅ Til o'zgartirildi: {lang_names.get(language, language)}\n\nEndi men {lang_names.get(language)} tilida javob beraman.",
                'es': f"✅ Idioma cambiado a: {lang_names.get(language, language)}\n\nAhora responderé en {lang_names.get(language)}."
            }
            
            # Edit message to show confirmation
            await telegram_bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=confirmations.get(language, confirmations['uz'])
            )
            
            # Answer callback query
            await telegram_bot.answer_callback_query(callback_query_data.get('id'), text="✅")
            
            return {'success': True, 'language': language}
        
        return {'success': False, 'error': 'Unknown callback data'}
        
    except Exception as e:
        print(f"Error handling language callback: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}
