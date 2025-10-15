"""
Webhook'ni tezda tuzatish
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.bot import Bot
from app.models.user import User
from app.services.telegram_service import delete_webhook, run_async

def fix_webhook():
    app = create_app()
    
    with app.app_context():
        # Admin user'ni topish
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        # Barcha botlarni olish
        bots = Bot.query.filter_by(user_id=user.id).all()
        
        for bot in bots:
            if bot.telegram_token_1:
                print(f"🔧 {bot.name} botini tuzatish...")
                
                # Avval eski webhook'ni o'chirish
                print("🗑️ Eski webhook o'chirilmoqda...")
                delete_result = run_async(delete_webhook(bot.telegram_token_1))
                
                if delete_result['success']:
                    print("✅ Eski webhook o'chirildi")
                else:
                    print(f"⚠️ Webhook o'chirishda muammo: {delete_result.get('error', 'Nomalum')}")
                
                print(f"🤖 Bot: @{bot.name}")
                print(f"🆔 Bot ID: {bot.id}")
                print(f"🔗 Webhook URL kerak: https://your-domain.com/telegram/webhook/{bot.id}")
                print("=" * 50)
        
        print("\n💡 Webhook o'rnatish uchun:")
        print("1. Ngrok ishga tushiring: ngrok http 5000")
        print("2. Yoki webhook setup sahifasiga kiring:")
        for bot in bots:
            if bot.telegram_token_1:
                print(f"   http://127.0.0.1:5000/telegram/setup/{bot.id}")

if __name__ == '__main__':
    fix_webhook()
