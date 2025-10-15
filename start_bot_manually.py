"""
Botni qo'lda ishga tushirish
"""
import sys
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.bot_manager import BotManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Database setup
db = SQLAlchemy()

class Bot:
    """Bot model"""
    def __init__(self, data):
        self.id = data[0]
        self.user_id = data[1] 
        self.name = data[2]
        self.description = data[3]
        self.telegram_token = data[4]
        self.telegram_username = data[5]
        self.language = data[6]
        self.system_prompt = data[7]
        self.is_active = data[8]
        self.admin_chat_id = data[9] if len(data) > 9 else None
        self.notification_channel = data[10] if len(data) > 10 else None
        self.notifications_enabled = data[11] if len(data) > 11 else False
        self.created_at = data[12] if len(data) > 12 else None
        self.total_messages = 0
        self.today_messages = 0

# Flask app yaratish
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/botfactory.db'
db.init_app(app)

with app.app_context():
    # Bot Manager yaratish
    bot_manager = BotManager(db)
    
    # Database'dan botni olish
    conn = sqlite3.connect('instance/botfactory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bots WHERE is_active = 1 LIMIT 1")
    bot_data = cursor.fetchone()
    conn.close()
    
    bot = Bot(bot_data) if bot_data else None
    
    if bot:
        print(f"✅ Bot topildi: {bot.name}")
        print(f"   Token: ***{bot.telegram_token[-10:]}")
        print(f"   Status: {'FAOL' if bot.is_active else 'NOFAOL'}")
        
        # Botni ishga tushirish
        result = bot_manager.start_bot(bot)
        
        if result['success']:
            print(f"✅ {result['message']}")
            print("\n🎉 BOT ISHGA TUSHDI!")
            print(f"Telegram'da @{bot.telegram_username} ga /start yuboring!")
            
            # Bot ishlashi uchun kutish
            print("\nBot ishlayapti... To'xtatish uchun Ctrl+C bosing")
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nBotni to'xtatish...")
                bot_manager.stop_bot(bot.id)
        else:
            print(f"❌ {result['message']}")
    else:
        print("❌ Bot topilmadi!")
