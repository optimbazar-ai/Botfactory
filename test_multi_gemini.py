"""
Ko'p API key va model almashish tizimini test qilish
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
except ImportError:
    print("dotenv topilmadi, muhit o'zgaruvchilarini to'g'ridan-to'g'ri o'qiyapman...")
    load_dotenv = lambda: None

import google.generativeai as genai

# .env faylini yuklash
load_dotenv()

# API keys va modellar
api_keys = [
    os.getenv('GEMINI_API_KEY'),
    os.getenv('GEMINI_API_KEY_2')
]

models = [
    'gemini-2.5-flash',      # Eng tez model
    'gemini-2.0-flash',      # Zaxira model 1
    'gemini-2.5-flash-lite', # Zaxira model 2
]

print("🔄 Ko'p Model va API Key Test")
print("=" * 50)

# Test xabar
test_message = "Salom! Qisqacha javob ber: 2+2 necha?"

# Barcha kombinatsiyalarni sinab ko'rish
success = False

for model_name in models:
    for i, api_key in enumerate(api_keys, 1):
        if not api_key or api_key == 'your-second-api-key-here':
            print(f"⚠️ API Key #{i} mavjud emas, o'tkazib yuborildi")
            continue
        
        try:
            print(f"\n📝 Sinash: Model={model_name}, Key=#{i}")
            
            # API sozlash
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            # Javob olish
            response = model.generate_content(test_message)
            
            print(f"✅ Muvaffaqiyatli!")
            print(f"   Model: {model_name}")
            print(f"   Key: #{i}")
            print(f"   Javob: {response.text[:100]}")
            success = True
            break  # Muvaffaqiyatli bo'lsa to'xtatamiz
            
        except Exception as e:
            error = str(e)
            if 'quota' in error.lower() or 'limit' in error.lower():
                print(f"❌ Limit tugagan!")
            elif 'not found' in error.lower():
                print(f"❌ Model topilmadi!")
            else:
                print(f"❌ Xatolik: {error[:100]}")
    
    if success:
        break

print("\n" + "=" * 50)

if success:
    print("✅ Test muvaffaqiyatli yakunlandi!")
    print("💡 Tizim ishlayapti - limit tugaganda avtomatik boshqa model/key ga o'tadi")
else:
    print("❌ Hech qaysi kombinatsiya ishlamadi")
    print("💡 Yordam:")
    print("1. .env faylidagi API keylarni tekshiring")
    print("2. Ikkinchi API key qo'shing: GEMINI_API_KEY_2=...")
    print("3. API limitlarini tekshiring")
