"""
Ngrok bilan webhook sozlash
"""
import os
import sys
import requests
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.bot import BotModel

def setup_ngrok_webhook():
    """
    Ngrok URL bilan webhook sozlash
    """
    app = create_app()
    
    with app.app_context():
        print("🌐 Ngrok Webhook Setup")
        print("=" * 40)
        
        # Get ngrok URL
        try:
            # Ngrok API dan URL olish
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()['tunnels']
            
            https_url = None
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    https_url = tunnel['public_url']
                    break
            
            if not https_url:
                print("❌ Ngrok HTTPS tunnel topilmadi!")
                print("💡 Ngrok ishga tushiring: ngrok http 5000")
                return
                
            print(f"✅ Ngrok URL topildi: {https_url}")
            
        except Exception as e:
            print("❌ Ngrok API'ga ulanib bo'lmadi!")
            print("💡 Ngrok ishga tushiring: ngrok http 5000")
            print(f"   Xatolik: {e}")
            return
        
        # Get all bots
        bots = BotModel.query.all()
        
        if not bots:
            print("❌ Hech qanday bot topilmadi!")
            return
        
        print(f"\n📋 {len(bots)} ta bot topildi:")
        for i, bot in enumerate(bots, 1):
            tokens = bot.get_telegram_tokens()
            status = "✅" if tokens else "❌"
            print(f"   {i}. {bot.name} (ID: {bot.id}) {status}")
        
        # Select bot
        try:
            bot_num = int(input("\n🎯 Qaysi bot uchun webhook sozlamoqchisiz? (raqam): "))
            selected_bot = bots[bot_num - 1]
        except (ValueError, IndexError):
            print("❌ Noto'g'ri raqam!")
            return
        
        # Check bot token
        tokens = selected_bot.get_telegram_tokens()
        if not tokens:
            print("❌ Bot'da Telegram token yo'q!")
            return
        
        bot_token = tokens[0]
        webhook_url = f"{https_url}/telegram/webhook/{selected_bot.id}"
        
        print(f"\n🔗 Webhook URL: {webhook_url}")
        
        # Set webhook
        try:
            telegram_api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
            data = {'url': webhook_url}
            
            response = requests.post(telegram_api_url, data=data)
            result = response.json()
            
            if result.get('ok'):
                print("✅ Webhook muvaffaqiyatli o'rnatildi!")
                print(f"📱 Bot'ni Telegram'da test qiling: @{selected_bot.name}")
            else:
                print(f"❌ Webhook o'rnatishda xatolik: {result.get('description')}")
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    setup_ngrok_webhook()
