"""
Botni web API orqali ishga tushirish
"""
import requests
from requests.auth import HTTPBasicAuth

# Login qilish
session = requests.Session()

# Login
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=False)

if response.status_code in [200, 302]:
    print("✅ Login muvaffaqiyatli!")
    
    # Bot ishga tushirish
    response = session.post('http://localhost:5000/bot/1/start')
    
    if response.status_code in [200, 302]:
        print("✅ BOT ISHGA TUSHDI!")
        print("\n🎉 TAYYOR!")
        print("Telegram'da @meningchatbotim_bot ga /start yuboring!")
    else:
        print(f"❌ Bot ishga tushmadi: {response.status_code}")
else:
    print("❌ Login xato!")
