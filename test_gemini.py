"""
Gemini API ni test qilish
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env faylini yuklash
load_dotenv()

# API key olish
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY .env faylida yo'q!")
    print("📝 Quyidagi qadamlarni bajaring:")
    print("1. https://makersuite.google.com/app/apikey ga o'ting")
    print("2. API key yarating")
    print("3. .env fayliga qo'shing: GEMINI_API_KEY=your-key-here")
    exit(1)

# Gemini'ni sozlash
genai.configure(api_key=api_key)

try:
    # Model yaratish (eng yangi model)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Test xabar
    prompt = "Salom! Men kimman?"
    
    print("🤖 Gemini API test")
    print(f"📝 Savol: {prompt}")
    print("⏳ Javob kutilmoqda...")
    
    # Javob olish
    response = model.generate_content(prompt)
    
    print("✅ Javob:")
    print(response.text)
    
    print("\n✅ Gemini API ishlayapti!")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    print("\n💡 Yordam:")
    print("1. API key to'g'riligini tekshiring")
    print("2. Internet aloqangizni tekshiring")
    print("3. Google AI Studio'da API key faolligini tekshiring")
