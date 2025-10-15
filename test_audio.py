from app import create_app
from app.services.audio_service import text_to_speech, get_language_code

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Gemini TTS Model Test")
    print("=" * 60)
    
    # Test 1: Text-to-Speech (Uzbek)
    print("\n1. Gemini TTS (O'zbek) testi:")
    test_text = "Salom! Men sizning virtual yordamchingizman."
    
    try:
        audio_bytes = text_to_speech(test_text, 'uz-UZ')
        if audio_bytes:
            # Save to file
            with open('test_audio_uz.mp3', 'wb') as f:
                f.write(audio_bytes)
            print(f"   ✅ Audio yaratildi: {len(audio_bytes)} bytes")
            print(f"   📁 Fayl saqlandi: test_audio_uz.mp3")
        else:
            print("   ❌ Audio yaratilmadi")
    except Exception as e:
        print(f"   ❌ Xatolik: {str(e)}")
    
    # Test 2: Text-to-Speech (Russian)
    print("\n2. Text-to-Speech (Русский) testi:")
    test_text_ru = "Здравствуйте! Я ваш виртуальный помощник. Чем могу помочь?"
    
    try:
        audio_bytes = text_to_speech(test_text_ru, 'ru-RU')
        if audio_bytes:
            with open('test_audio_ru.mp3', 'wb') as f:
                f.write(audio_bytes)
            print(f"   ✅ Audio yaratildi: {len(audio_bytes)} bytes")
            print(f"   📁 Fayl saqlandi: test_audio_ru.mp3")
        else:
            print("   ❌ Audio yaratilmadi")
    except Exception as e:
        print(f"   ❌ Xatolik: {str(e)}")
    
    # Test 3: Text-to-Speech (English)
    print("\n3. Text-to-Speech (English) testi:")
    test_text_en = "Hello! I am your virtual assistant. How can I help you?"
    
    try:
        audio_bytes = text_to_speech(test_text_en, 'en-US')
        if audio_bytes:
            with open('test_audio_en.mp3', 'wb') as f:
                f.write(audio_bytes)
            print(f"   ✅ Audio yaratildi: {len(audio_bytes)} bytes")
            print(f"   📁 Fayl saqlandi: test_audio_en.mp3")
        else:
            print("   ❌ Audio yaratilmadi")
    except Exception as e:
        print(f"   ❌ Xatolik: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Audio fayllarni eshiting va tekshiring!")
    print("=" * 60)
