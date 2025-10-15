"""
Haqiqiy Telegram bot bilan test
"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.bot import Bot
from app.models.user import User
from app.services.telegram_service import get_bot_info, set_webhook, delete_webhook, run_async

def test_real_bot():
    app = create_app()
    
    with app.app_context():
        # Admin user'ni topish
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        # Barcha botlarni ko'rsatish
        bots = Bot.query.filter_by(user_id=user.id).all()
        
        if not bots:
            print("❌ Hech qanday bot topilmadi!")
            print("💡 Avval saytda bot yarating: http://127.0.0.1:5000/bots/new")
            return
        
        print("📋 Mavjud botlar:")
        for i, bot in enumerate(bots, 1):
            token_status = "✅ Bor" if bot.telegram_token_1 else "❌ Yo'q"
            active_status = "✅ Faol" if bot.is_active else "❌ Faol emas"
            print(f"   {i}. {bot.name} - Token: {token_status}, Holat: {active_status}")
        
        # Birinchi botni test qilish
        test_bot = bots[0]
        print(f"\n🧪 '{test_bot.name}' botini test qilish...")
        
        if not test_bot.telegram_token_1:
            print("❌ Bot tokensi yo'q! Avval token qo'shing.")
            return
        
        if not test_bot.is_active:
            print("❌ Bot faol emas! Avval faollashtiring.")
            return
        
        # Bot ma'lumotlarini olish
        print("📡 Bot ma'lumotlarini olish...")
        bot_info_result = run_async(get_bot_info(test_bot.telegram_token_1))
        
        if bot_info_result['success']:
            bot_info = bot_info_result['bot']
            print(f"✅ Bot topildi: @{bot_info.get('username', 'N/A')}")
            print(f"   Nomi: {bot_info.get('first_name', 'N/A')}")
            print(f"   ID: {bot_info.get('id', 'N/A')}")
        else:
            error_msg = bot_info_result.get('error', 'Nomalum xato')
            print(f"❌ Bot ma'lumotlarini olishda xato: {error_msg}")
            return
        
        # Webhook URL'ini yaratish
        webhook_url = f"https://your-domain.com/telegram/webhook/{test_bot.id}"
        print(f"\n🔗 Webhook URL: {webhook_url}")
        print("⚠️  Haqiqiy webhook o'rnatish uchun HTTPS domain kerak!")
        
        # Test webhook (localhost)
        local_webhook = f"http://127.0.0.1:5000/telegram/webhook/{test_bot.id}"
        print(f"🏠 Local webhook: {local_webhook}")
        
        print("\n✅ Bot tayyor!")
        print("📱 Telegram'da botingizga /start yuboring")
        print(f"🌐 Yoki webhook setup sahifasiga kiring: http://127.0.0.1:5000/telegram/setup/{test_bot.id}")

if __name__ == '__main__':
    test_real_bot()
