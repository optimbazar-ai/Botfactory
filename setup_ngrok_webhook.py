"""
Ngrok yordamida webhook sozlash
"""
import sys
import os
import requests
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.bot import Bot
from app.models.user import User
from app.services.telegram_service import set_webhook, delete_webhook, run_async

def setup_ngrok_webhook():
    app = create_app()
    
    with app.app_context():
        # Admin user'ni topish
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        # Birinchi botni olish
        bot = Bot.query.filter_by(user_id=user.id).first()
        if not bot:
            print("❌ Bot topilmadi!")
            return
        
        if not bot.telegram_token_1:
            print("❌ Bot tokensi yo'q!")
            return
        
        print(f"🤖 Bot: {bot.name}")
        print(f"🔑 Token: {bot.telegram_token_1[:10]}...")
        
        # Ngrok tunnel ma'lumotlarini olish
        try:
            ngrok_api = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
            tunnels = ngrok_api.json()
            
            https_tunnel = None
            for tunnel in tunnels.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    https_tunnel = tunnel.get('public_url')
                    break
            
            if not https_tunnel:
                print("❌ Ngrok HTTPS tunnel topilmadi!")
                print("💡 Ngrok'ni ishga tushiring:")
                print("   ngrok http 5000")
                return
            
            print(f"🌐 Ngrok URL: {https_tunnel}")
            
            # Webhook URL yaratish
            webhook_url = f"{https_tunnel}/telegram/webhook/{bot.id}"
            print(f"🔗 Webhook URL: {webhook_url}")
            
            # Webhook o'rnatish
            print("📡 Webhook o'rnatilmoqda...")
            result = run_async(set_webhook(bot.telegram_token_1, webhook_url))
            
            if result['success']:
                print("✅ Webhook muvaffaqiyatli o'rnatildi!")
                print(f"📱 Telegram'da @{bot.name} botiga /start yuboring")
            else:
                error_msg = result.get('error', 'Nomalum xato')
                print(f"❌ Webhook o'rnatishda xato: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Ngrok API'ga ulanib bo'lmadi!")
            print("💡 Ngrok ishga tushganligini tekshiring:")
            print("   ngrok http 5000")
        except Exception as e:
            print(f"❌ Xato: {e}")

def delete_current_webhook():
    """Joriy webhook'ni o'chirish"""
    app = create_app()
    
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        bot = Bot.query.filter_by(user_id=user.id).first()
        if not bot or not bot.telegram_token_1:
            print("❌ Bot yoki token topilmadi!")
            return
        
        print("🗑️ Webhook o'chirilmoqda...")
        result = run_async(delete_webhook(bot.telegram_token_1))
        
        if result['success']:
            print("✅ Webhook muvaffaqiyatli o'chirildi!")
        else:
            error_msg = result.get('error', 'Nomalum xato')
            print(f"❌ Webhook o'chirishda xato: {error_msg}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'delete':
        delete_current_webhook()
    else:
        print("🚀 Ngrok webhook sozlash")
        print("=" * 30)
        setup_ngrok_webhook()
        print("\n💡 Webhook o'chirish uchun: python setup_ngrok_webhook.py delete")
