"""
Manual webhook o'rnatish
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.bot import Bot
from app.models.user import User
from app.services.telegram_service import set_webhook, run_async

def set_webhook_manual():
    app = create_app()
    
    with app.app_context():
        # Admin user'ni topish
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        # Birinchi botni olish
        bot = Bot.query.filter_by(user_id=user.id).first()
        if not bot or not bot.telegram_token_1:
            print("❌ Bot yoki token topilmadi!")
            return
        
        print(f"🤖 Bot: {bot.name}")
        print(f"🆔 Bot ID: {bot.id}")
        
        # HTTPS URL so'rash
        print("\n🌐 HTTPS URL kiriting (masalan: https://your-domain.com)")
        print("💡 Ngrok: ngrok http 5000 (keyin https://xxx.ngrok.io)")
        print("💡 CloudFlare Tunnel, localtunnel.me, serveo.net ham ishlatishingiz mumkin")
        
        https_url = input("HTTPS URL: ").strip()
        
        if not https_url:
            print("❌ URL kiritilmadi!")
            return
        
        if not https_url.startswith('https://'):
            print("❌ URL https:// bilan boshlanishi kerak!")
            return
        
        # Webhook URL yaratish
        webhook_url = f"{https_url}/telegram/webhook/{bot.id}"
        print(f"\n🔗 Webhook URL: {webhook_url}")
        
        # Webhook o'rnatish
        print("📡 Webhook o'rnatilmoqda...")
        result = run_async(set_webhook(bot.telegram_token_1, webhook_url))
        
        if result['success']:
            print("✅ Webhook muvaffaqiyatli o'rnatildi!")
            print(f"📱 Telegram'da botingizga /start yuboring: @{bot.name}")
        else:
            error_msg = result.get('error', 'Nomalum xato')
            print(f"❌ Webhook o'rnatishda xato: {error_msg}")

if __name__ == '__main__':
    set_webhook_manual()
