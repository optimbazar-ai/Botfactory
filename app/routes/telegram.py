from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, csrf
from app.models.bot import Bot
from app.services.telegram_service import (
    process_telegram_message,
    process_voice_message,
    run_async,
    set_webhook,
    delete_webhook,
    get_bot_info
)

telegram_bp = Blueprint('telegram', __name__, url_prefix='/telegram')


@telegram_bp.route('/webhook/<int:bot_id>', methods=['POST'])
@csrf.exempt
def webhook(bot_id):
    """
    Telegram webhook endpoint for receiving messages.
    
    This endpoint receives updates from Telegram and processes them.
    Each bot has its own webhook URL.
    """
    try:
        # Get the update data from Telegram
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({'error': 'No data received'}), 400
        
        # Find the bot in database
        bot = Bot.query.get(bot_id)
        
        if not bot:
            return jsonify({'error': 'Bot not found'}), 404
        
        if not bot.is_active:
            return jsonify({'error': 'Bot is inactive'}), 403
        
        # Check for callback query (language selection)
        callback_query = update_data.get('callback_query')
        if callback_query:
            from app.services.telegram_service import handle_language_callback
            
            message = callback_query.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            message_id = message.get('message_id')
            
            if chat_id and message_id:
                result = run_async(
                    handle_language_callback(bot, callback_query, chat_id, message_id)
                )
                return jsonify({'ok': True}), 200
        
        # Extract message from update
        message = update_data.get('message')
        
        if not message:
            # Not a message update (could be callback, inline query, etc.)
            return jsonify({'ok': True}), 200
        
        # Get chat ID and user ID
        chat = message.get('chat')
        if not chat:
            return jsonify({'error': 'No chat in message'}), 400
        
        chat_id = chat.get('id')
        user = message.get('from')
        telegram_user_id = user.get('id') if user else None
        
        # Check if it's a voice message
        voice = message.get('voice')
        
        if voice:
            # Process voice message
            voice_file_id = voice.get('file_id')
            print(f"🎤 Received voice message from chat {chat_id}")
            
            result = run_async(
                process_voice_message(bot, voice_file_id, chat_id, telegram_user_id)
            )
        else:
            # Get message text
            message_text = message.get('text')
            
            if not message_text:
                # No text in message (could be photo, sticker, etc.)
                return jsonify({'ok': True}), 200
            
            # Process text message
            result = run_async(
                process_telegram_message(bot, message_text, chat_id, telegram_user_id)
            )
        
        if result['success']:
            return jsonify({'ok': True}), 200
        else:
            # Still return 200 to Telegram so it doesn't retry
            print(f"Error processing message: {result.get('error')}")
            return jsonify({'ok': True}), 200
            
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        # Return 200 to prevent Telegram from retrying
        return jsonify({'ok': True}), 200


@telegram_bp.route('/setup/<int:bot_id>', methods=['GET', 'POST'])
@login_required
def setup_webhook(bot_id):
    """Setup webhook for a bot."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'set_webhook':
            # Get webhook URL from environment or config
            # In production, this should be your public domain
            base_url = request.form.get('webhook_url', '').strip()
            
            if not base_url:
                flash('Please provide webhook URL', 'danger')
                return redirect(url_for('telegram.setup_webhook', bot_id=bot_id))
            
            # Construct full webhook URL
            webhook_url = f"{base_url}/telegram/webhook/{bot_id}"
            
            # Set webhook
            tokens = bot.get_telegram_tokens()
            if not tokens:
                flash('Bot does not have any Telegram tokens configured', 'danger')
                return redirect(url_for('telegram.setup_webhook', bot_id=bot_id))
            result = run_async(set_webhook(tokens[0], webhook_url))
            
            if result['success']:
                flash(f'Webhook set successfully to: {webhook_url}', 'success')
            else:
                flash(f"Failed to set webhook: {result.get('error')}", 'danger')
                
        elif action == 'delete_webhook':
            tokens = bot.get_telegram_tokens()
            if not tokens:
                flash('Bot does not have any Telegram tokens configured', 'danger')
                return redirect(url_for('telegram.setup_webhook', bot_id=bot_id))
            result = run_async(delete_webhook(tokens[0]))
            
            if result['success']:
                flash('Webhook deleted successfully', 'success')
            else:
                flash(f"Failed to delete webhook: {result.get('error')}", 'danger')
        
        return redirect(url_for('telegram.setup_webhook', bot_id=bot_id))
    
    # GET request - show setup page
    bot_info = None
    webhook_info = None
    
    tokens = bot.get_telegram_tokens()
    if tokens:
        # Get bot info
        bot_info_result = run_async(get_bot_info(tokens[0]))
        if bot_info_result['success']:
            bot_info = bot_info_result['bot']
        
        # Get current webhook info
        try:
            from telegram import Bot as TelegramBot
            telegram_bot = TelegramBot(token=tokens[0])
            webhook_data = run_async(telegram_bot.get_webhook_info())
            webhook_info = {
                'url': webhook_data.url,
                'pending_update_count': webhook_data.pending_update_count,
                'last_error_message': webhook_data.last_error_message,
                'last_error_date': webhook_data.last_error_date
            }
        except Exception as e:
            print(f"Error getting webhook info: {e}")
    
    return render_template(
        'telegram/setup.html',
        bot=bot,
        bot_info=bot_info,
        webhook_info=webhook_info
    )


@telegram_bp.route('/test/<int:bot_id>', methods=['GET', 'POST'])
@login_required
def test_bot(bot_id):
    """Test bot with a sample message."""
    bot = Bot.query.get_or_404(bot_id)
    
    # Check ownership
    if bot.user_id != current_user.id:
        flash('You do not have permission to access this bot', 'danger')
        return redirect(url_for('bot.list_bots'))
    
    response_data = None
    error = None
    
    if request.method == 'POST':
        message_text = request.form.get('message', '').strip()
        test_chat_id = request.form.get('chat_id', '12345').strip()
        
        if not message_text:
            error = 'Please enter a message'
        elif not bot.get_telegram_tokens():
            error = 'Bot does not have any Telegram tokens configured'
        else:
            try:
                result = run_async(
                    process_telegram_message(bot, message_text, int(test_chat_id))
                )
                
                if result['success']:
                    response_data = {
                        'message': message_text,
                        'response': result['response']
                    }
                else:
                    error = result.get('error', 'Unknown error')
            except Exception as e:
                error = str(e)
    
    return render_template(
        'telegram/test.html',
        bot=bot,
        response=response_data,
        error=error
    )
