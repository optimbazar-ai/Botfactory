"""
TTS funksiyasini test qilish
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.audio_service import text_to_speech

def test_tts():
    app = create_app()
    
    with app.app_context():
        print("🔊 TTS funksiyasini test qilish...")
        
        # Test matn
        test_text = "Assalomu alaykum! Men sizning yordamchi botingizman."
        
        print(f"📝 Test matn: {test_text}")
        print("🎵 Audio yaratilmoqda...")
        
        # TTS chaqirish
        audio_data = text_to_speech(test_text, 'uz-UZ')
        
        if audio_data and len(audio_data) > 0:
            print(f"✅ Audio yaratildi: {len(audio_data)} bytes")
            
            # Audio faylni saqlash
            with open('test_audio.wav', 'wb') as f:
                f.write(audio_data)
            print("💾 Audio fayl saqlandi: test_audio.wav")
            
        else:
            print("❌ Audio yaratilmadi!")
            print("🔍 Muammo sabablar:")
            print("   - Google API key noto'g'ri")
            print("   - Internet aloqasi yo'q")
            print("   - TTS service ishlamayapti")

if __name__ == '__main__':
    test_tts()
