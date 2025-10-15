"""
Bot loglarini tekshirish
"""
import time
import requests

print("🔍 BOT LOGLARINI TEKSHIRISH")
print("=" * 50)

# Flask app holatini tekshirish
try:
    response = requests.get("http://localhost:5000", timeout=2)
    print("✅ Flask app ishlayapti")
except:
    print("❌ Flask app ishlamayapti!")
    exit(1)

# Bot holatini tekshirish
session = requests.Session()

login_data = {
    'username': 'admin',
    'password': 'admin123'
}

response = session.post('http://localhost:5000/login', data=login_data)
if response.status_code == 200:
    print("✅ Login muvaffaqiyatli")
    
    # Bot sahifasini olish
    response = session.get('http://localhost:5000/bot/1')
    
    if 'Faol' in response.text or 'FAOL' in response.text:
        print("✅ Bot FAOL holatda")
    else:
        print("❌ Bot NOFAOL holatda")
        print("\n💡 YECHIM: python restart_bot.py")

print("\n📊 NATIJA:")
print("Agar bot faol bo'lsa:")
print("1. Telegram'da /start yuboring")
print("2. Tugmalarni bosing")
print("3. Tugma ishlashi kerak!")
print("\nAgar ishlamasa:")
print("- Bot loglarini terminalda kuzating")
print("- Flask app terminali xatoliklarni ko'rsatadi")
