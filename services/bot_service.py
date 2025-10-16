"""
Telegram Bot Service - Polling orqali ishlaydi
"""
import asyncio
import threading
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters
import google.generativeai as genai
from services.gemini_tts import GeminiTTS  # Gemini TTS o'rniga
from services.knowledge_base import KnowledgeBase  # Bilimlar bazasi
import speech_recognition as sr
import io
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API sozlash (agar mavjud bo'lsa)
gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
if gemini_key:
    genai.configure(api_key=gemini_key)
    print("✅ Gemini API key topildi va sozlandi")
else:
    print("⚠️ GEMINI_API_KEY yoki GOOGLE_API_KEY o'rnatilmagan - Bot oddiy rejimda ishlaydi")


class TelegramBotService:
    """Telegram bot xizmatlari"""
    
    def __init__(self, bot_model, db):
        """Bot service yaratish"""
        self.bot_model = bot_model
        self.db = db
        self.application = None
        self.running = False
        self.thread = None
        
        # Gemini API tekshirish
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.gemini_available = bool(gemini_key)
        if not self.gemini_available:
            print("⚠️ GEMINI_API_KEY yoki GOOGLE_API_KEY yo'q - oddiy javoblar ishlatiladi")
        
        # API keys va modellar ro'yxati (barcha mavjud keylarni yig'ish)
        self.api_keys = [
            os.getenv('GEMINI_API_KEY'),
            os.getenv('GOOGLE_API_KEY'),
            os.getenv('GEMINI_API_KEY_2')
        ]
        # Bo'sh keylarni olib tashlash
        self.api_keys = [key for key in self.api_keys if key and key != 'your-second-api-key-here']
        self.models = [
            'gemini-2.5-flash',      # Eng tez model
            'gemini-2.0-flash',      # Zaxira model 1
            'gemini-2.5-flash-lite', # Zaxira model 2
        ]
        
        # Hozirgi key va model indeksi
        self.current_key_index = 0
        self.current_model_index = 0
        
        # Gemini TTS service
        self.tts_service = GeminiTTS()
        
        # Bilimlar bazasi
        self.knowledge_base = KnowledgeBase(bot_model.id, db)
        
        # Spam detection
        self.message_times = {}
        
    async def start_polling(self):
        """Bot polling'ni boshlash"""
        if not self.bot_model.telegram_token:
            return False
            
        try:
            # Application yaratish
            self.application = Application.builder().token(self.bot_model.telegram_token).build()
            
            # Handlerlar qo'shish
            self.application.add_handler(CommandHandler("start", self.handle_start))
            self.application.add_handler(CommandHandler("uz", self.handle_lang_uz))
            self.application.add_handler(CommandHandler("ru", self.handle_lang_ru))
            self.application.add_handler(CommandHandler("en", self.handle_lang_en))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
            self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
            
            # Polling boshlash
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            self.running = True
            print(f"✅ Bot ishga tushdi: @{self.bot_model.telegram_username}")
            return True
            
        except Exception as e:
            print(f"❌ Bot ishga tushishda xatolik: {e}")
            return False
    
    async def stop_polling(self):
        """Bot polling'ni to'xtatish"""
        if self.application and self.running:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self.running = False
            print(f"🛑 Bot to'xtatildi: @{self.bot_model.telegram_username}")
    
    async def handle_start(self, update: Update, context):
        """Start komandasi"""
        user = update.effective_user
        
        # Foydalanuvchi tilini tekshirish
        user_language = self.get_user_language(user.id)
        
        if not user_language:
            # Til tanlanmagan - oddiy matn bilan
            await update.message.reply_text(
                "👋 **Tilni tanlang / Выберите язык / Choose language:**\n\n"
                "🇺🇿 O'zbek tili uchun: /uz\n"
                "🇷🇺 Для русского: /ru\n"
                "🇬🇧 For English: /en"
            )
        else:
            # Til tanlangan, xush kelibsiz xabari
            welcome_text = self.get_welcome_message(user.first_name, user_language)
            await update.message.reply_text(welcome_text)
        
        # Statistika yangilash
        self.update_statistics()
    
    async def handle_lang_uz(self, update: Update, context):
        """O'zbek tilini tanlash"""
        user = update.effective_user
        self.save_user_language(user.id, 'uz')
        welcome_text = self.get_welcome_message(user.first_name, 'uz')
        await update.message.reply_text(welcome_text)
        print(f"✅ User {user.id} o'zbek tilini tanladi")
    
    async def handle_lang_ru(self, update: Update, context):
        """Rus tilini tanlash"""
        user = update.effective_user
        self.save_user_language(user.id, 'ru')
        welcome_text = self.get_welcome_message(user.first_name, 'ru')
        await update.message.reply_text(welcome_text)
        print(f"✅ User {user.id} rus tilini tanladi")
    
    async def handle_lang_en(self, update: Update, context):
        """Ingliz tilini tanlash"""
        user = update.effective_user
        self.save_user_language(user.id, 'en')
        welcome_text = self.get_welcome_message(user.first_name, 'en')
        await update.message.reply_text(welcome_text)
        print(f"✅ User {user.id} ingliz tilini tanladi")
    
    async def handle_message(self, update: Update, context):
        """Matnli xabarlarni qayta ishlash"""
        user = update.effective_user
        message_text = update.message.text
        chat_id = update.effective_chat.id
        
        # Foydalanuvchi tilini olish
        user_language = self.get_user_language(user.id)
        if not user_language:
            user_language = self.bot_model.language  # Default til
        
        # Admin/kanalga xabarni forward qilish
        await self.forward_to_admin(user, message_text, is_user_message=True)
        
        # Spam tekshirish
        is_spam = await self.check_spam(user.id, message_text)
        if is_spam:
            spam_messages = {
                'uz': "⚠️ Juda ko'p xabar yuboryapsiz! Biroz kuting.",
                'ru': "⚠️ Вы отправляете слишком много сообщений! Подождите немного.",
                'en': "⚠️ You're sending too many messages! Please wait."
            }
            await update.message.reply_text(spam_messages.get(user_language, spam_messages['uz']))
            self.log_spam(user, message_text)
            return
        
        # Xabar limiti tekshirish  
        if not self.check_message_limit():
            await update.message.reply_text(
                "❌ Xabar limiti tugadi!\n\n"
                "Premium rejimga o'tish uchun admin bilan bog'laning:\n"
                "📞 +998996448444\n"
                "💬 @Akramjon1984"
            )
            return
        
        # Avval bilimlar bazasidan qidirish
        kb_response = self.knowledge_base.find_answer(message_text)
        
        if kb_response:
            # Bilimlar bazasidan javob topildi
            await update.message.reply_text(f"📚 {kb_response}")
            final_response = kb_response
        else:
            # AI javob olish (user tilida)
            ai_response = await self.get_ai_response_with_knowledge(message_text, user_language)
            await update.message.reply_text(ai_response)
            final_response = ai_response
        
        # Audio javob YOQILMAGAN
        
        # Xabarni saqlash va statistika
        self.save_message(user, message_text, final_response)
        self.update_statistics()
        
        # Bot javobini admin/kanalga forward qilish
        await self.forward_to_admin(user, final_response, is_user_message=False)
    
    async def handle_voice(self, update: Update, context):
        """Ovozli xabarlarni qayta ishlash"""
        user = update.effective_user
        
        # Foydalanuvchi tilini olish
        user_language = self.get_user_language(user.id)
        if not user_language:
            user_language = self.bot_model.language
        
        try:
            # Ovozli faylni yuklab olish
            voice = update.message.voice
            file = await voice.get_file()
            voice_bytes = await file.download_as_bytearray()
            
            print(f"🎤 Ovozli xabar qabul qilindi (User: {user.id}, Til: {user_language})")
            
            # Speech to text
            text = self.speech_to_text(voice_bytes, user_language)
            
            if not text:
                error_messages = {
                    'uz': "🎤 Ovozingizni tushuna olmadim. Qaytadan urinib ko'ring yoki matn yuboring.",
                    'ru': "🎤 Не удалось распознать голос. Попробуйте еще раз или отправьте текст.",
                    'en': "🎤 Could not recognize your voice. Please try again or send text."
                }
                await update.message.reply_text(error_messages.get(user_language, error_messages['uz']))
                return
            
            print(f"✅ Ovoz matnga aylandi: {text}")
            
            # Matnni ko'rsatish
            await update.message.reply_text(f"📝 Siz aytdingiz: _{text}_", parse_mode='Markdown')
            
            # AI javob olish
            ai_response = await self.get_ai_response_with_knowledge(text, user_language)
            
            # Matn javobini yuborish
            await update.message.reply_text(ai_response)
            
            print(f"✅ Matn javobi yuborildi")
            
            # Audio javob YOQILMAGAN
            
            # Xabarni saqlash
            self.save_message(user, text, ai_response)
            self.update_statistics()
            
            # Admin/kanalga forward
            await self.forward_to_admin(user, f"🎤 Ovozli: {text}", is_user_message=True)
            await self.forward_to_admin(user, ai_response, is_user_message=False)
            
        except Exception as e:
            print(f"❌ Ovozli xabar xatolik: {e}")
            import traceback
            traceback.print_exc()
            
            error_msg = {
                'uz': "❌ Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.",
                'ru': "❌ Произошла ошибка. Пожалуйста, попробуйте еще раз.",
                'en': "❌ An error occurred. Please try again."
            }
            await update.message.reply_text(error_msg.get(user_language, error_msg['uz']))
    
    async def handle_audio(self, update: Update, context):
        """Audio xabarlarni qayta ishlash"""
        await self.handle_voice(update, context)
    
    async def get_ai_response_with_knowledge(self, message, language='uz'):
        """AI javob olish (bilimlar bazasi bilan)"""
        # Bilimlar bazasini prompt ga qo'shish
        knowledge_context = self.knowledge_base.export_to_prompt()
        
        # Til bo'yicha ko'rsatma
        language_instructions = {
            'uz': "Javobni O'ZBEK tilida bering.",
            'ru': "Отвечайте на РУССКОМ языке.",
            'en': "Answer in ENGLISH."
        }
        
        lang_instruction = language_instructions.get(language, language_instructions['uz'])
        
        # To'liq prompt yaratish
        full_prompt = f"{self.bot_model.system_prompt}\n\n{knowledge_context}\n\n{lang_instruction}\n\nFoydalanuvchi: {message}\nJavob:"
        
        return await self.get_ai_response(full_prompt, is_full_prompt=True)
    
    async def get_ai_response(self, message, is_full_prompt=False):
        """Gemini AI dan javob olish (model va key almashish bilan)"""
        # Agar Gemini API yo'q bo'lsa, oddiy javoblar
        if not self.gemini_available:
            return self.get_fallback_response(message)
        
        # Prompt tayyorlash
        if is_full_prompt:
            prompt = message  # To'liq prompt berilgan
        else:
            prompt = f"{self.bot_model.system_prompt}\n\nFoydalanuvchi: {message}\nJavob:"
        
        # Barcha model va key kombinatsiyalarini sinab ko'rish
        for model_name in self.models:
            for api_key in self.api_keys:
                if not api_key or api_key == 'your-second-api-key-here':
                    continue
                
                try:
                    # API key va model sozlash
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name)
                    
                    # Javob olishga urinish
                    response = model.generate_content(prompt)
                    
                    print(f"✅ Model ishlatildi: {model_name} (Key #{self.api_keys.index(api_key)+1})")
                    return response.text
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    
                    # Limit tugagan yoki model mavjud emas
                    if 'quota' in error_msg or 'limit' in error_msg or 'not found' in error_msg:
                        print(f"⚠️ {model_name} limit tugagan yoki topilmadi (Key #{self.api_keys.index(api_key)+1})")
                        continue  # Keyingi key/modelga o'tish
                    
                    # Boshqa xatoliklar
                    print(f"❌ AI xatolik ({model_name}): {e}")
                    continue
        
        # Hech qaysi model ishlamasa
        print("❌ Barcha model va keylar sinab ko'rildi, hech biri ishlamadi")
        return "Kechirasiz, hozircha javob bera olmayman. Keyinroq urinib ko'ring."
    
    def get_fallback_response(self, message):
        """Gemini API yo'q bo'lganda oddiy javoblar"""
        message_lower = message.lower()
        
        # Oddiy javoblar lug'ati
        responses = {
            'salom': 'Salom! Sizga qanday yordam bera olaman?',
            'hello': 'Hello! How can I help you?',
            'привет': 'Привет! Чем могу помочь?',
            'qanday': 'Men yaxshiman, rahmat!',
            'kim': f"Men {self.bot_model.name} botiman.",
            'yordam': 'Sizga qanday yordam kerak?',
            'help': 'How can I assist you?',
            'помощь': 'Чем могу помочь?',
            '/start': f"Xush kelibsiz! Men {self.bot_model.name} botiman.",
        }
        
        # Bilimlar bazasidan javob izlash
        kb_answer = self.knowledge_base.find_answer(message)
        if kb_answer:
            return kb_answer
        
        # Oddiy javoblardan mosini topish
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        # Default javob
        return f"Sizning xabaringiz: {message}\n\nBot hozircha oddiy javob rejimida ishlayapti."
    
    def text_to_speech(self, text, language='uz'):
        """Matnni ovozga aylantirish (Gemini TTS)"""
        try:
            # Gemini TTS bilan ovoz yaratish
            # Til asosida ovoz tanlash
            voice_map = {
                'uz': 'Kore',    # O'zbek uchun Kore ovozi yaxshi
                'ru': 'Aoede',   # Rus tili uchun
                'en': 'Puck'     # Ingliz tili uchun
            }
            voice_name = voice_map.get(language, 'Kore')
            
            # Audio yaratish (MP3 formatda)
            audio_bytes = self.tts_service.text_to_speech(text, voice_name)
            
            if audio_bytes:
                # Telegram uchun BytesIO buffer yaratish
                audio_buffer = io.BytesIO(audio_bytes)
                audio_buffer.seek(0)
                return audio_buffer
            else:
                print(f"⚠️ Gemini TTS ishlamadi, oddiy TTS ishlatilmoqda")
                # Zaxira variant - oddiy TTS (agar kerak bo'lsa)
                from gtts import gTTS
                lang_codes = {'uz': 'tr', 'ru': 'ru', 'en': 'en'}
                tts = gTTS(text=text, lang=lang_codes.get(language, 'en'), slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                return audio_buffer
                
        except Exception as e:
            print(f"❌ TTS xatolik: {e}")
            return None
    
    def speech_to_text(self, audio_bytes, language='uz'):
        """Ovozni matnga aylantirish - Google Speech Recognition"""
        try:
            from pydub import AudioSegment
            import tempfile
            
            print(f"🎤 Speech-to-text boshlandi (Til: {language})")
            
            recognizer = sr.Recognizer()
            
            # Telegram OGG faylini WAV ga o'girish
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_ogg:
                temp_ogg.write(audio_bytes)
                temp_ogg_path = temp_ogg.name
            
            # OGG to WAV
            audio = AudioSegment.from_file(temp_ogg_path, format="ogg")
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
            
            audio.export(temp_wav_path, format="wav")
            
            # Speech recognition
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = recognizer.record(source)
            
            # Til kodlari - O'zbek uchun RUS ishlatamiz (yaxshiroq ishlaydi)
            lang_codes = {
                'uz': 'ru-RU',  # O'zbek uchun rus
                'ru': 'ru-RU',
                'en': 'en-US'
            }
            lang_code = lang_codes.get(language, 'ru-RU')
            
            print(f"🔍 Tanib olish: {lang_code}")
            
            # Google Speech Recognition
            text = recognizer.recognize_google(audio_data, language=lang_code)
            
            # Temp fayllarni o'chirish
            try:
                os.unlink(temp_ogg_path)
                os.unlink(temp_wav_path)
            except:
                pass
            
            if text:
                print(f"✅ Tanildi: {text}")
                return text
            else:
                print("⚠️ Matn tanimadi")
                return None
            
        except sr.UnknownValueError:
            print("❌ Ovozni tushunib bo'lmadi")
            return None
        except Exception as e:
            print(f"❌ STT xatolik: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _google_speech_recognition(self, audio_bytes, language='uz'):
        """Zaxira variant: Google Speech Recognition"""
        try:
            from pydub import AudioSegment
            import tempfile
            
            recognizer = sr.Recognizer()
            
            # OGG to WAV
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_ogg:
                temp_ogg.write(audio_bytes)
                temp_ogg_path = temp_ogg.name
            
            audio = AudioSegment.from_file(temp_ogg_path, format="ogg")
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
            
            audio.export(temp_wav_path, format="wav")
            
            # Speech recognition
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = recognizer.record(source)
            
            # Til kodlari
            lang_codes = {'uz': 'ru-RU', 'ru': 'ru-RU', 'en': 'en-US'}
            lang_code = lang_codes.get(language, 'ru-RU')
            
            text = recognizer.recognize_google(audio_data, language=lang_code)
            
            # Cleanup
            import os
            try:
                os.unlink(temp_ogg_path)
                os.unlink(temp_wav_path)
            except:
                pass
            
            return text
            
        except Exception as e:
            print(f"❌ Google STT xatolik: {e}")
            return None
    
    async def check_spam(self, user_id, message_text):
        """Spam tekshirish"""
        current_time = datetime.now()
        
        # Foydalanuvchi xabarlar vaqti
        if user_id not in self.message_times:
            self.message_times[user_id] = []
        
        # Oxirgi 1 daqiqadagi xabarlar
        self.message_times[user_id] = [
            t for t in self.message_times[user_id] 
            if (current_time - t).total_seconds() < 60
        ]
        
        # Yangi vaqt qo'shish
        self.message_times[user_id].append(current_time)
        
        # 1 daqiqada 10+ xabar = spam
        if len(self.message_times[user_id]) > 10:
            return True
        
        # Taqiqlangan so'zlar tekshirish
        banned_words = self.get_banned_words()
        message_lower = message_text.lower()
        
        for word in banned_words:
            if word.lower() in message_lower:
                return True
        
        return False
    
    def get_banned_words(self):
        """Taqiqlangan so'zlar ro'yxati"""
        # Bu yerda database'dan olish kerak
        return [
            'spam', 'reklama', 'click', 'payme',
            'casino', 'bukmekar', 'qimor'
        ]
    
    def check_message_limit(self):
        """Xabar limiti tekshirish (memory-based)"""
        # Oddiy - hamma uchun ruxsat
        return True
    
    def save_message(self, telegram_user, message_text, response_text):
        """Xabarni saqlash (memory-based)"""
        try:
            # Oddiy saqlash (database'siz)
            if not hasattr(self, 'messages_log'):
                self.messages_log = []
            
            self.messages_log.append({
                'user_id': telegram_user.id,
                'user_name': telegram_user.first_name,
                'message': message_text,
                'response': response_text,
                'timestamp': datetime.now()
            })
            
            print(f"💾 Xabar saqlandi ({len(self.messages_log)} ta)")
            
        except Exception as e:
            print(f"❌ Xabar saqlashda xatolik: {e}")
    
    def update_statistics(self):
        """Statistikani yangilash (memory-based)"""
        try:
            # Oddiy counter (database'siz)
            if not hasattr(self, 'message_count'):
                self.message_count = 0
            
            self.message_count += 1
            print(f"📊 Statistika: {self.message_count} ta xabar")
            
        except Exception as e:
            print(f"❌ Statistika xatolik: {e}")
    
    def log_spam(self, user, message):
        """Spam xabarni log qilish"""
        # Admin'ga xabar yuborish kerak
        print(f"⚠️ SPAM: User @{user.username} ({user.id}): {message[:50]}...")
    
    async def forward_to_admin(self, user, message_text, is_user_message=True):
        """Xabarni admin chat yoki kanalga forward qilish"""
        if not self.bot_model.notifications_enabled:
            return
        
        # Agar user admin bo'lsa, monitoring yubormaymiz
        if self.bot_model.admin_chat_id and str(user.id) == str(self.bot_model.admin_chat_id):
            return
        
        try:
            from telegram import Bot as TelegramBot
            bot = TelegramBot(token=self.bot_model.telegram_token)
            
            # Xabar formatini tayyorlash
            if is_user_message:
                formatted_message = f"""👤 **Mijoz:** @{user.username or 'Nomsiz'} ({user.first_name})
📩 **Xabar:** {message_text}
🤖 **Bot:** @{self.bot_model.telegram_username}
⏰ **Vaqt:** {datetime.now().strftime('%H:%M:%S')}"""
            else:
                formatted_message = f"""🤖 **Bot javobi:**
{message_text}
⏰ **Vaqt:** {datetime.now().strftime('%H:%M:%S')}"""
            
            # Admin chatga yuborish
            if self.bot_model.admin_chat_id:
                try:
                    await bot.send_message(
                        chat_id=self.bot_model.admin_chat_id,
                        text=formatted_message,
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    print(f"❌ Admin chatga yuborishda xatolik: {e}")
            
            # Kanalga yuborish
            if self.bot_model.notification_channel:
                try:
                    await bot.send_message(
                        chat_id=self.bot_model.notification_channel,
                        text=formatted_message,
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    print(f"❌ Kanalga yuborishda xatolik: {e}")
        
        except Exception as e:
            print(f"❌ Forward qilishda xatolik: {e}")
    
    async def handle_callback(self, update: Update, context):
        """Callback tugmalari (til tanlash)"""
        try:
            query = update.callback_query
            user = query.from_user
            
            print(f"🔔 Callback qabul qilindi: {query.data}")
            
            await query.answer()
            
            # Til tanlash
            if query.data.startswith("lang_"):
                language = query.data.split("_")[1]  # uz, ru, en
                
                print(f"✅ Til tanlandi: {language} (User: {user.id})")
                
                # Foydalanuvchi tilini saqlash
                self.save_user_language(user.id, language)
                
                # Xush kelibsiz xabari tanlangan tilda
                welcome_text = self.get_welcome_message(user.first_name, language)
                
                await query.edit_message_text(welcome_text)
                print(f"✅ Xabar yangilandi!")
                
        except Exception as e:
            print(f"❌ Callback xatolik: {e}")
            import traceback
            traceback.print_exc()
    
    def get_user_language(self, user_id):
        """Foydalanuvchi tilini olish"""
        try:
            # Memory cache'dan olish
            if not hasattr(self, 'user_languages'):
                self.user_languages = {}
            
            return self.user_languages.get(user_id, None)
        except:
            return None
    
    def save_user_language(self, user_id, language):
        """Foydalanuvchi tilini saqlash"""
        try:
            # Oddiy dictionary'da saqlash (memory cache)
            if not hasattr(self, 'user_languages'):
                self.user_languages = {}
            
            self.user_languages[user_id] = language
            print(f"✅ Til saqlandi: User {user_id} = {language}")
            
        except Exception as e:
            print(f"❌ Tilni saqlashda xatolik: {e}")
            import traceback
            traceback.print_exc()
    
    def get_welcome_message(self, name, language=None):
        """Xush kelibsiz xabari"""
        if not language:
            language = self.bot_model.language
        
        if language == 'uz':
            return f"""
Assalomu alaykum, {name}! 👋

Men {self.bot_model.name} botiman.
{self.bot_model.description or 'Sizga yordam berishga tayyorman!'}

Menga istalgan savolingizni yuboring.
Ovozli xabar ham yuborishingiz mumkin! 🎤
"""
        elif self.bot_model.language == 'ru':
            return f"""
Здравствуйте, {name}! 👋

Я бот {self.bot_model.name}.
{self.bot_model.description or 'Готов помочь вам!'}

Задавайте любые вопросы.
Можете отправить голосовое сообщение! 🎤
"""
        else:
            return f"""
Hello, {name}! 👋

I'm {self.bot_model.name} bot.
{self.bot_model.description or 'Ready to help you!'}

Ask me any questions.
You can send voice messages too! 🎤
"""
