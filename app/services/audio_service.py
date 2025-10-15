"""
Audio service for speech-to-text and text-to-speech functionality.
Uses Google Speech Recognition for transcription and Gemini TTS for text-to-speech.
"""
import os
import tempfile
import requests
import base64
import wave
import struct
try:
    import speech_recognition as sr
except ImportError:
    # Fallback if SpeechRecognition has issues
    sr = None
from io import BytesIO
try:
    from pydub import AudioSegment
except ImportError:
    # Fallback if pydub has issues with Python 3.13
    AudioSegment = None
from flask import current_app
import google.generativeai as genai


def transcribe_audio(audio_bytes: bytes, language_code: str = 'uz-UZ') -> str:
    """
    Convert speech audio to text - simplified version for production.
    
    Args:
        audio_bytes: Audio file content in bytes
        language_code: Language code
        
    Returns:
        str: Transcribed text or fallback message
    """
    # For now, return a simple message since audio processing is complex in production
    return "Audio transcription temporarily disabled"


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
    Convert text to speech audio using Gemini TTS model via REST API.

    Args:
        text: Text to convert to speech
        language_code: Language code (uz-UZ, ru-RU, en-US)
        
    Returns:
        bytes: Audio content in WAV format, or empty bytes if generation fails.
    """
    try:
        api_key = current_app.config['GOOGLE_API_KEY']
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

        print("🔊 Generating audio with Gemini TTS API...")
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
                            print(f"✅ Gemini TTS audio received: {len(pcm_data)} bytes (MIME: {mime_type})")

                            if 'pcm' in mime_type.lower() or 'L16' in mime_type:
                                print("🔄 Converting PCM to WAV...")
                                wav_data = pcm_to_wav(pcm_data, sample_rate=24000)
                                print(f"✅ WAV audio created: {len(wav_data)} bytes")
                                return wav_data
                            else:
                                return pcm_data
        
        print(f"⚠️ Gemini TTS failed (status: {response.status_code}, response: {response.text[:500]})")
        return b''

    except Exception as e:
        print(f"❌ Gemini TTS error: {str(e)}")
        import traceback
        traceback.print_exc()
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
