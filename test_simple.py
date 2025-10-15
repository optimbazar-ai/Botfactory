"""
Oddiy test - API key va Gemini ishlashini tekshirish
"""
import os

# API keyni to'g'ridan-to'g'ri .env faylidan o'qish
env_path = os.path.join(os.path.dirname(__file__), '.env')

api_key = None
api_key_2 = None

try:
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                parts = line.strip().split('=', 1)
                if len(parts) == 2:
                    if 'GEMINI_API_KEY_2' in line:
                        api_key_2 = parts[1]
                    else:
                        api_key = parts[1]
except:
    print("❌ .env faylini o'qib bo'lmadi")
    exit(1)

print("📋 API Keylar:")
print(f"   Key #1: {'✅ Mavjud' if api_key else '❌ Yo\'q'}")
print(f"   Key #2: {'✅ Mavjud' if api_key_2 and api_key_2 != 'your-second-api-key-here' else '❌ Yo\'q'}")

# Gemini test
try:
    import google.generativeai as genai
    
    if api_key:
        print("\n🔄 Gemini test qilinmoqda...")
        genai.configure(api_key=api_key)
        
        # Model yaratish
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Test
        response = model.generate_content("Qisqacha javob: 2+2=?")
        print(f"✅ Gemini ishlayapti! Javob: {response.text.strip()}")
    else:
        print("\n❌ API key yo'q!")
        
except ImportError:
    print("❌ google-generativeai kutubxonasi topilmadi")
except Exception as e:
    print(f"❌ Xatolik: {e}")
