"""
Telegram Bot Polling Service - webhook o'rniga
"""
import asyncio
import threading
import time
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from flask import current_app
from app.services.telegram_service import handle_message
from app.models.bot import BotModel

class BotPollingManager:
    """Bot polling manager - barcha botlarni boshqaradi"""
    
    def __init__(self):
        self.running_bots = {}  # bot_id -> thread
        self.stop_flags = {}    # bot_id -> stop_flag
    
    def start_bot(self, bot_model):
        """Botni ishga tushirish"""
        bot_id = bot_model.id
        
        if bot_id in self.running_bots:
            return {'success': False, 'error': 'Bot allaqachon ishlamoqda'}
        
        # Get bot token
        tokens = bot_model.get_telegram_tokens()
        if not tokens:
            return {'success': False, 'error': 'Bot token topilmadi'}
        
        # Create stop flag
        stop_flag = threading.Event()
        self.stop_flags[bot_id] = stop_flag
        
        # Start polling thread
        thread = threading.Thread(
            target=self._poll_bot,
            args=(bot_model, tokens[0], stop_flag),
            daemon=True
        )
        thread.start()
        
        self.running_bots[bot_id] = thread
        
        return {'success': True, 'message': 'Bot ishga tushdi'}
    
    def stop_bot(self, bot_id):
        """Botni to'xtatish"""
        if bot_id not in self.running_bots:
            return {'success': False, 'error': 'Bot ishlamayapti'}
        
        # Set stop flag
        self.stop_flags[bot_id].set()
        
        # Wait for thread to finish
        self.running_bots[bot_id].join(timeout=5)
        
        # Clean up
        del self.running_bots[bot_id]
        del self.stop_flags[bot_id]
        
        return {'success': True, 'message': 'Bot to\'xtatildi'}
    
    def is_bot_running(self, bot_id):
        """Bot ishlab turganligini tekshirish"""
        return bot_id in self.running_bots
    
    def get_running_bots(self):
        """Ishlab turgan botlar ro'yxati"""
        return list(self.running_bots.keys())
    
    def _poll_bot(self, bot_model, token, stop_flag):
        """Bot polling - alohida thread'da ishlaydi"""
        try:
            # Create bot instance
            bot = Bot(token=token)
            last_update_id = 0
            
            print(f"🤖 Bot polling boshlandi: {bot_model.name}")
            
            while not stop_flag.is_set():
                try:
                    # Get updates
                    updates = bot.get_updates(
                        offset=last_update_id + 1,
                        timeout=10,
                        limit=10
                    )
                    
                    for update in updates:
                        if update.message:
                            # Process message
                            asyncio.run(self._handle_update(bot_model, update.message))
                        
                        last_update_id = update.update_id
                    
                    # Small delay
                    time.sleep(1)
                    
                except TelegramError as e:
                    print(f"❌ Telegram xatolik ({bot_model.name}): {e}")
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"❌ Umumiy xatolik ({bot_model.name}): {e}")
                    time.sleep(5)
            
            print(f"🛑 Bot polling to'xtatildi: {bot_model.name}")
            
        except Exception as e:
            print(f"❌ Bot polling xatolik: {e}")
    
    async def _handle_update(self, bot_model, message):
        """Telegram xabarini qayta ishlash"""
        try:
            # Convert telegram message to dict
            message_dict = {
                'message_id': message.message_id,
                'from': {
                    'id': message.from_user.id,
                    'first_name': message.from_user.first_name,
                    'username': message.from_user.username
                },
                'chat': {
                    'id': message.chat.id,
                    'type': message.chat.type
                },
                'text': message.text,
                'date': message.date.timestamp() if message.date else time.time()
            }
            
            # Handle message
            result = await handle_message(bot_model, message_dict)
            
            if not result.get('success'):
                print(f"❌ Xabar qayta ishlashda xatolik: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Update handle xatolik: {e}")

# Global polling manager
polling_manager = BotPollingManager()
