"""
Gemini TTS Service - O'zbek tilida mukammal talaffuz
"""
import os
import base64
import io
import json
import requests
from typing import Optional

# pydub Python 3.13 da muammo - optional qilamiz
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    print("⚠️ pydub yuklanmadi - audioop moduli Python 3.13 da o'chirilgan")
    PYDUB_AVAILABLE = False

class GeminiTTS:
    """Gemini TTS xizmati - gtts dan ancha yaxshi talaffuz"""
    
    def __init__(self, api_key: str = None):
        """
        Gemini TTS ni ishga tushirish
        
        Args:
            api_key: Gemini API key (agar berilmasa muhitdan oladi)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # TTS API endpoint
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
        
    def text_to_speech(self, text: str, voice_name: str = "Kore") -> Optional[bytes]:
        """
        Matnni ovozga aylantirish (Gemini TTS REST API)
        
        Args:
            text: Ovozga aylantirilishi kerak bo'lgan matn
            voice_name: Ovoz nomi (Kore, Puck, Charon, Fenrir, Aoede)
            
        Returns:
            Audio bytes (MP3 format) yoki None agar xatolik bo'lsa
        """
        try:
            if not self.api_key:
                print("❌ API key mavjud emas!")
                return None
            
            # API URL with key
            url = f"{self.api_url}?key={self.api_key}"
            
            # Request payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f'"{text}"'  # Matnni qo'shtirnoq ichiga olish muhim
                    }]
                }],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": voice_name
                            }
                        }
                    }
                }
            }
            
            # API ga so'rov
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                # Audio ma'lumotlarni olish
                if 'candidates' in result and result['candidates']:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        part = candidate['content']['parts'][0]
                        if 'inlineData' in part:
                            audio_data = part['inlineData']['data']  # base64 encoded PCM
                            mime_type = part['inlineData']['mimeType']
                            
                            # PCM ni MP3 ga o'girish
                            audio_bytes = self.convert_pcm_to_mp3(audio_data, mime_type)
                            
                            return audio_bytes
            else:
                print(f"❌ API xatolik: {response.status_code} - {response.text}")
            
            return None
            
        except Exception as e:
            print(f"❌ Gemini TTS xatolik: {e}")
            return None
    
    def pcm_to_mp3(self, base64_pcm: str, mime_type: str) -> Optional[bytes]:
        """
        PCM audio ni MP3 ga konvertatsiya qilish
        
        Args:
            base64_pcm: Base64 kodirlangan PCM audio
            mime_type: MIME turi (sample rate uchun)
            
        Returns:
            MP3 audio bytes
        """
        if not PYDUB_AVAILABLE:
            print("⚠️ pydub mavjud emas - PCM audio qaytarilmoqda")
            # PCM audio'ni qaytaramiz (MP3 o'rniga)
            return base64.b64decode(base64_pcm)
            
        try:
            # Base64 dan bytes ga
            pcm_bytes = base64.b64decode(base64_pcm)
            
            # Sample rate ni olish (masalan: audio/x-pcm;rate=24000)
            sample_rate = 24000  # default
            if 'rate=' in mime_type:
                rate_str = mime_type.split('rate=')[1].split(';')[0]
                sample_rate = int(rate_str)
            
            # PCM ni AudioSegment ga yuklash
            # PCM 16-bit signed integer deb faraz qilamiz
            audio = AudioSegment(
                pcm_bytes,
                frame_rate=sample_rate,
                sample_width=2,  # 16-bit = 2 bytes
                channels=1  # mono
            )
            
            # MP3 ga eksport
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format='mp3', bitrate='128k')
            mp3_buffer.seek(0)
            
            return mp3_buffer.read()
            
        except Exception as e:
            print(f"❌ PCM konversiya xatolik: {e}")
            return None
    
    def get_available_voices(self):
        """Mavjud ovozlar ro'yxati"""
        return [
            {
                "name": "Kore",
                "description": "Ayol ovozi, yumshoq va tushunarli",
                "recommended": True
            },
            {
                "name": "Puck", 
                "description": "Erkak ovozi, rasmiy"
            },
            {
                "name": "Charon",
                "description": "Erkak ovozi, chuqur"
            },
            {
                "name": "Fenrir",
                "description": "Erkak ovozi, kuchli"
            },
            {
                "name": "Aoede",
                "description": "Ayol ovozi, jonli"
            }
        ]


# Test funksiyasi
if __name__ == "__main__":
    # .env faylidan API key olish
    from dotenv import load_dotenv
    load_dotenv()
    
    # TTS yaratish
    tts = GeminiTTS()
    
    # Test matn
    test_text = "Assalomu alaykum! Men Gemini TTS xizmatiman. O'zbek tilida juda yaxshi gaplasha olaman."
    
    print("🎤 Gemini TTS Test")
    print(f"📝 Matn: {test_text}")
    print("⏳ Audio yaratilmoqda...")
    
    # Audio yaratish
    audio_bytes = tts.text_to_speech(test_text)
    
    if audio_bytes:
        # Faylga saqlash (test uchun)
        with open("test_gemini_tts.mp3", "wb") as f:
            f.write(audio_bytes)
        print("✅ Audio tayyor: test_gemini_tts.mp3")
        
        # Mavjud ovozlar
        print("\n📋 Mavjud ovozlar:")
        for voice in tts.get_available_voices():
            mark = "⭐" if voice.get("recommended") else "  "
            print(f"{mark} {voice['name']}: {voice['description']}")
    else:
        print("❌ Audio yaratib bo'lmadi")
