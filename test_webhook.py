"""
Webhook va bot funksiyalarini test qilish
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

def test_webhook():
    app = create_app()
    
    with app.app_context():
        # Test user va bot yaratish
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Admin user topilmadi!")
            return
        
        # Test bot yaratish yoki mavjudini topish
        test_bot = Bot.query.filter_by(user_id=user.id).first()
        
        if not test_bot:
            # Yangi test bot yaratish
            test_bot = Bot(
                user_id=user.id,
                name="Test Bot",
                description="Test uchun bot",
                language="uz",
                platform="telegram",
                system_prompt="Sen do'stona va foydali yordamchi botsan.",
                telegram_token_1="TEST_TOKEN_123",  # Test token
                is_active=True
            )
            db.session.add(test_bot)
            db.session.commit()
            print(f"✅ Test bot yaratildi: ID {test_bot.id}")
        else:
            print(f"✅ Mavjud bot topildi: ID {test_bot.id}")
        
        # Webhook URL'ini test qilish
        webhook_url = f"http://127.0.0.1:5000/telegram/webhook/{test_bot.id}"
        print(f"🔗 Webhook URL: {webhook_url}")
        
        # Test message yaratish
        test_message = {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 12345,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "testuser"
                },
                "chat": {
                    "id": 12345,
                    "first_name": "Test",
                    "username": "testuser",
                    "type": "private"
                },
                "date": 1634567890,
                "text": "/start"
            }
        }
        
        print("\n🧪 Webhook'ni test qilish...")
        
        try:
            # Webhook'ga test message yuborish
            response = requests.post(
                webhook_url,
                json=test_message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"📊 Response status: {response.status_code}")
            print(f"📄 Response content: {response.text}")
            
            if response.status_code == 200:
                print("✅ Webhook muvaffaqiyatli ishladi!")
            else:
                print("❌ Webhook'da muammo bor!")
                
        except requests.exceptions.ConnectionError:
            print("❌ Server ishlamayapti yoki ulanish muammosi!")
        except requests.exceptions.Timeout:
            print("❌ Webhook javob berish vaqti tugadi!")
        except Exception as e:
            print(f"❌ Kutilmagan xato: {e}")
        
        # Bot ma'lumotlarini ko'rsatish
        print(f"\n📋 Bot ma'lumotlari:")
        print(f"   ID: {test_bot.id}")
        print(f"   Nomi: {test_bot.name}")
        print(f"   Til: {test_bot.language}")
        token_status = '✅ Bor' if test_bot.telegram_token_1 else '❌ Yoq'
        active_status = '✅ Ha' if test_bot.is_active else '❌ Yoq'
        print(f"   Token: {token_status}")
        print(f"   Faol: {active_status}")

if __name__ == '__main__':
    test_webhook()
