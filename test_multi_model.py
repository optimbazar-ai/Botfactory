"""
Ko'p model va API key almashish tizimini test qilish
"""
import os
import google.generativeai as genai

# .env faylidan API keylarni o'qish
def load_api_keys():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    api_keys = []
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if 'GEMINI_API_KEY' in line and '=' in line:
                    key = line.strip().split('=', 1)[1]
                    if key and key != 'your-second-api-key-here':
                        api_keys.append(key)
    except:
        print("❌ .env faylini o'qib bo'lmadi")
    
    return api_keys

# Model va key almashish tizimi
def get_ai_response_with_fallback(message):
    """Model va API key almashish bilan javob olish"""
    
    # API keylar
    api_keys = load_api_keys()
    
    # Model ro'yxati (limiti kam bo'lganidan ko'pga qarab)
    models = [
        'gemini-2.5-flash',      # Eng tez model
        'gemini-2.0-flash',      # Zaxira model 1
        'gemini-2.5-flash-lite', # Zaxira model 2
        'gemini-2.5-pro',        # Eng kuchli model
    ]
    
    print(f"📋 Mavjud API keylar: {len(api_keys)} ta")
    print(f"📋 Sinab ko'riladigan modellar: {len(models)} ta")
    print("=" * 50)
    
    # Barcha kombinatsiyalarni sinab ko'rish
    attempt = 0
    for model_name in models:
        for i, api_key in enumerate(api_keys, 1):
            attempt += 1
            print(f"\n🔄 Urinish #{attempt}: Model={model_name}, Key=#{i}")
            
            try:
                # API key va model sozlash
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                # Javob olish
                response = model.generate_content(message)
                
                print(f"✅ MUVAFFAQIYAT!")
                print(f"   Model: {model_name}")
                print(f"   Key: #{i}")
                return {
                    'success': True,
                    'model': model_name,
                    'key_index': i,
                    'response': response.text
                }
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if 'quota' in error_msg or 'limit' in error_msg:
                    print(f"   ❌ Limit tugagan!")
                elif 'not found' in error_msg:
                    print(f"   ❌ Model topilmadi!")
                elif '429' in error_msg:
                    print(f"   ❌ Rate limit!")
                else:
                    print(f"   ❌ Xatolik: {str(e)[:100]}")
                
                continue
    
    return {
        'success': False,
        'message': 'Barcha model va keylar sinab ko\'rildi, hech biri ishlamadi'
    }

# Test
if __name__ == "__main__":
    print("🧪 Ko'p Model va API Key Almashish Tizimi")
    print("=" * 50)
    
    # Test xabar
    test_message = "Qisqacha javob ber: O'zbekiston poytaxti qaysi shahar?"
    
    print(f"\n📝 Test savol: {test_message}")
    print("=" * 50)
    
    # Javob olish
    result = get_ai_response_with_fallback(test_message)
    
    print("\n" + "=" * 50)
    print("📊 NATIJA:")
    
    if result['success']:
        print(f"✅ Muvaffaqiyatli!")
        print(f"   Model: {result['model']}")
        print(f"   Key indeksi: #{result['key_index']}")
        print(f"   Javob: {result['response'][:200]}")
        print("\n💡 Xulosa: Limit tugaganda avtomatik boshqa model/key ga o'tadi!")
    else:
        print(f"❌ {result['message']}")
        print("\n💡 Yechim:")
        print("1. Ikkinchi API key qo'shing: GEMINI_API_KEY_2=...")
        print("2. API limitlarini tekshiring")
        print("3. Model nomlarini yangilang")
