"""
Oddiy audio test - Flask app'siz
"""
import os
from gtts import gTTS
import io

def test_google_tts():
    """Google TTS'ni test qilish"""
    print("🔊 Google TTS Test")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        ("Assalomu alaykum! Men sizning yordamchi botingizman.", "tr", "uzbek"),
        ("Привет! Я ваш помощник бот.", "ru", "russian"),
        ("Hello! I am your assistant bot.", "en", "english"),
        ("¡Hola! Soy tu bot asistente.", "es", "spanish")
    ]
    
    for i, (text, lang, name) in enumerate(test_cases, 1):
        print(f"\n{i}. {name.title()} test:")
        print(f"   Matn: {text}")
        
        try:
            # Create TTS
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to file
            filename = f"test_{name}.mp3"
            tts.save(filename)
            
            # Check file size
            size = os.path.getsize(filename)
            print(f"   ✅ Muvaffaqiyatli: {size} bytes")
            print(f"   💾 Fayl: {filename}")
            
        except Exception as e:
            print(f"   ❌ Xatolik: {e}")
    
    print(f"\n{'='*30}")
    print("🎵 Test tugadi!")
    print("💡 MP3 fayllarni media player bilan oching")

if __name__ == '__main__':
    test_google_tts()
