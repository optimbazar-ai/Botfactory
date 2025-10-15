"""
Botni to'liq qayta ishga tushirish
"""
import requests
import time

session = requests.Session()

# Login
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

print("🔄 BOTNI QAYTA ISHGA TUSHIRISH")
print("=" * 50)

response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=False)

if response.status_code in [200, 302]:
    print("✅ Login muvaffaqiyatli!")
    
    # Avval to'xtatish
    print("\n1️⃣ Botni to'xtatish...")
    response = session.post('http://localhost:5000/bot/1/stop')
    
    if response.status_code in [200, 302]:
        print("✅ Bot to'xtatildi!")
    
    # 2 sekund kutish
    print("\n⏳ 2 sekund kutilmoqda...")
    time.sleep(2)
    
    # Qayta ishga tushirish
    print("\n2️⃣ Botni qayta ishga tushirish...")
    response = session.post('http://localhost:5000/bot/1/start')
    
    if response.status_code in [200, 302]:
        print("✅ BOT QAYTA ISHGA TUSHDI!")
        print("\n🎉 TAYYOR!")
        print("\n📱 ENDI TELEGRAM'DA TEST QILING:")
        print("1. /start yuboring")
        print("2. Til tanlang (tugmani bosing)")
        print("3. Tugma ishlashi kerak!")
    else:
        print(f"❌ Bot ishga tushmadi: {response.status_code}")
else:
    print("❌ Login xato!")
