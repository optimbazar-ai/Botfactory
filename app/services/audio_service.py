"""
Audio service for text-to-speech functionality.
Uses Google TTS and Gemini for audio generation.
"""
import os
import tempfile
import requests
import base64
import wave
import struct
import io
from flask import current_app
import google.generativeai as genai
from gtts import gTTS


def transcribe_audio(audio_bytes: bytes, language_code: str = 'uz-UZ') -> str:
    """
    Convert speech audio to text - vaqtincha o'chirilgan.
    
    Args:
        audio_bytes: Audio file content in bytes
        language_code: Language code
        
    Returns:
        str: Transcribed text or fallback message
    """
    return "🎤 Ovozli xabarlarni tushunish vaqtincha o'chirilgan. Matn yozing."


def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000, channels: int = 1, sample_width: int = 2) -> bytes:
    """
    Convert raw PCM audio to WAV format.
    
    Args:
        pcm_data: Raw PCM audio bytes
        sample_rate: Sample rate in Hz (default: 24000)
        channels: Number of audio channels (default: 1 for mono)
        sample_width: Sample width in bytes (default: 2 for 16-bit)
        
    Returns:
        bytes: WAV format audio
    """
    wav_buffer = BytesIO()
    
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)
    
    wav_buffer.seek(0)
    return wav_buffer.read()


def text_to_speech(text: str, language_code: str = 'uz-UZ') -> bytes:
    """
    Convert text to speech audio using multiple TTS services.
    1. Try Gemini TTS (premium quality)
    2. Fallback to Google TTS (reliable)

    Args:
        text: Text to convert to speech
        language_code: Language code (uz-UZ, ru-RU, en-US)
        
    Returns:
        bytes: Audio content in WAV/MP3 format
    """
    print(f"🔊 TTS so'rovi: '{text[:50]}...' ({language_code})")
    
    # Try Gemini TTS first
    gemini_audio = _try_gemini_tts(text, language_code)
    if gemini_audio:
        return gemini_audio
    
    # Fallback to Google TTS
    print("🔄 Gemini TTS ishlamadi, Google TTS'ga o'tish...")
    return _try_google_tts(text, language_code)


def _try_gemini_tts(text: str, language_code: str) -> bytes:
    """Gemini TTS'ni sinab ko'rish"""
    try:
        api_key = current_app.config.get('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY topilmadi")
            return b''
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"

        payload = {
            "contents": [{"parts": [{"text": f'"{text}"'}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": "Kore"
                        }
                    }
                }
            }
        }

        headers = {"Content-Type": "application/json"}

        print("🔊 Gemini TTS bilan audio yaratilmoqda...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part:
                            audio_data = part['inlineData']['data']
                            mime_type = part['inlineData'].get('mimeType', '')
                            pcm_data = base64.b64decode(audio_data)
                            print(f"✅ Gemini TTS muvaffaqiyatli: {len(pcm_data)} bytes")

                            if 'pcm' in mime_type.lower() or 'L16' in mime_type:
                                wav_data = pcm_to_wav(pcm_data, sample_rate=24000)
                                return wav_data
                            else:
                                return pcm_data
        
        print(f"⚠️ Gemini TTS xatolik: {response.status_code}")
        return b''

    except Exception as e:
        print(f"❌ Gemini TTS xatolik: {str(e)}")
        return b''


def _try_google_tts(text: str, language_code: str) -> bytes:
    """Google TTS'ni sinab ko'rish (fallback)"""
    try:
        # Language mapping for Google TTS
        lang_map = {
            'uz-UZ': 'tr',  # Uzbek yo'q, Turkish yaqin
            'ru-RU': 'ru',
            'en-US': 'en',
            'es-ES': 'es'
        }
        
        lang = lang_map.get(language_code, 'en')
        
        print(f"🔊 Google TTS bilan audio yaratilmoqda ({lang})...")
        
        # Create TTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to bytes
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        audio_data = audio_buffer.read()
        print(f"✅ Google TTS muvaffaqiyatli: {len(audio_data)} bytes")
        
        return audio_data
        
    except Exception as e:
        print(f"❌ Google TTS xatolik: {str(e)}")
        return b''


def get_language_code(language: str) -> str:
    """
    Convert language code to full language-region code.
    
    Args:
        language: Short language code (en, ru, uz, es)
        
    Returns:
        str: Full language code (en-US, ru-RU, uz-UZ, es-ES)
    """
    language_map = {
        'en': 'en-US',
        'ru': 'ru-RU',
        'uz': 'uz-UZ',
        'es': 'es-ES'
    }
    return language_map.get(language, 'uz-UZ')
