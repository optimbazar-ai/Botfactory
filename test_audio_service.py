"""
Audio service test - TTS funksiyasini sinash
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.audio_service import text_to_speech

def test_audio_service():
    """Audio service'ni test qilish"""
    app = create_app()
    
    with app.app_context():
        print("🔊 Audio Service Test")
        print("=" * 40)
        
        # Test texts in different languages
        test_cases = [
            ("Assalomu alaykum! Men sizning yordamchi botingizman.", "uz-UZ"),
            ("Привет! Я ваш помощник бот.", "ru-RU"),
            ("Hello! I am your assistant bot.", "en-US"),
            ("¡Hola! Soy tu bot asistente.", "es-ES")
        ]
        
        for i, (text, lang) in enumerate(test_cases, 1):
            print(f"\n{i}. Test: {lang}")
            print(f"   Matn: {text}")
            
            try:
                # Generate audio
                audio_data = text_to_speech(text, lang)
                
                if audio_data and len(audio_data) > 0:
                    # Save audio file
                    filename = f"test_audio_{lang.replace('-', '_').lower()}.mp3"
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    
                    print(f"   ✅ Muvaffaqiyatli: {len(audio_data)} bytes")
                    print(f"   💾 Saqlandi: {filename}")
                else:
                    print(f"   ❌ Audio yaratilmadi!")
                    
            except Exception as e:
                print(f"   ❌ Xatolik: {e}")
        
        print("\n" + "=" * 40)
        print("🎵 Test tugadi!")
        print("💡 Audio fayllarni tinglang va sifatini tekshiring")

if __name__ == '__main__':
    test_audio_service()
