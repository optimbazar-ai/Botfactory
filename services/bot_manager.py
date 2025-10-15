"""
Bot Manager - Barcha botlarni boshqarish
"""
import asyncio
import threading
from services.bot_service import TelegramBotService


class BotManager:
    """Barcha botlarni boshqarish"""
    
    def __init__(self, db):
        self.db = db
        self.running_bots = {}  # bot_id: TelegramBotService
        self.threads = {}  # bot_id: Thread
    
    def start_bot(self, bot_model):
        """Botni ishga tushirish"""
        if bot_model.id in self.running_bots:
            return {'success': False, 'message': 'Bot allaqachon ishlayapti'}
        
        if not bot_model.telegram_token:
            return {'success': False, 'message': 'Telegram token kiritilmagan'}
        
        try:
            # Bot service yaratish
            bot_service = TelegramBotService(bot_model, self.db)
            
            # Alohida thread'da ishga tushirish
            thread = threading.Thread(
                target=self.run_bot_async,
                args=(bot_service,),
                daemon=True
            )
            thread.start()
            
            # Saqlash
            self.running_bots[bot_model.id] = bot_service
            self.threads[bot_model.id] = thread
            
            # Bot statusini yangilash
            bot_model.is_active = True
            self.db.session.commit()
            
            return {
                'success': True, 
                'message': f'Bot muvaffaqiyatli ishga tushdi: @{bot_model.telegram_username}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Xatolik: {str(e)}'
            }
    
    def stop_bot(self, bot_id):
        """Botni to'xtatish"""
        if bot_id not in self.running_bots:
            return {'success': False, 'message': 'Bot ishlamayapti'}
        
        try:
            bot_service = self.running_bots[bot_id]
            
            # Bot'ni to'xtatish
            asyncio.run(bot_service.stop_polling())
            
            # Ro'yxatdan o'chirish
            del self.running_bots[bot_id]
            del self.threads[bot_id]
            
            # Bot statusini yangilash
            from app import Bot
            bot = Bot.query.get(bot_id)
            if bot:
                bot.is_active = False
                self.db.session.commit()
            
            return {
                'success': True,
                'message': 'Bot to\'xtatildi'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Xatolik: {str(e)}'
            }
    
    def restart_bot(self, bot_id):
        """Botni qayta ishga tushirish"""
        self.stop_bot(bot_id)
        
        from app import Bot
        bot_model = Bot.query.get(bot_id)
        if bot_model:
            return self.start_bot(bot_model)
        
        return {'success': False, 'message': 'Bot topilmadi'}
    
    def get_bot_status(self, bot_id):
        """Bot holatini olish"""
        if bot_id in self.running_bots:
            return {
                'running': True,
                'status': 'Ishlayapti'
            }
        return {
            'running': False,
            'status': 'To\'xtatilgan'
        }
    
    def get_all_running_bots(self):
        """Barcha ishlab turgan botlar"""
        return list(self.running_bots.keys())
    
    def stop_all_bots(self):
        """Barcha botlarni to'xtatish"""
        bot_ids = list(self.running_bots.keys())
        for bot_id in bot_ids:
            self.stop_bot(bot_id)
    
    def run_bot_async(self, bot_service):
        """Bot'ni async rejimda ishga tushirish"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(bot_service.start_polling())
            
            # Bot ishlashda davom etsin
            while bot_service.running:
                loop.run_until_complete(asyncio.sleep(1))
                
        except Exception as e:
            print(f"❌ Bot thread xatolik: {e}")
        finally:
            loop.close()


# Global bot manager
bot_manager = None

def init_bot_manager(db):
    """Bot manager'ni ishga tushirish"""
    global bot_manager
    bot_manager = BotManager(db)
    return bot_manager
