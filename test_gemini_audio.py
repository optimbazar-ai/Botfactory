"""
Test Gemini TTS audio format and quality
"""
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# API Key
API_KEY = os.environ.get('GOOGLE_API_KEY')

def test_gemini_tts(text):
    """Test Gemini TTS API directly"""
    
    # API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
    
    # Payload
    payload = {
        "model": "gemini-2.5-flash-preview-tts",
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "response_modalities": ["AUDIO"]
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    print(f"Testing Gemini TTS...")
    print(f"Text: {text}")
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        # Extract audio
        if 'candidates' in result:
            for candidate in result['candidates']:
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part:
                            audio_data = part['inlineData']['data']
                            mime_type = part['inlineData'].get('mimeType', 'unknown')
                            
                            audio_bytes = base64.b64decode(audio_data)
                            
                            print(f"✅ Audio received!")
                            print(f"   Size: {len(audio_bytes)} bytes")
                            print(f"   MIME type: {mime_type}")
                            
                            # Check magic bytes
                            magic = audio_bytes[:16]
                            print(f"   Magic bytes: {magic.hex()}")
                            
                            # Determine file extension
                            if audio_bytes[:4] == b'RIFF':
                                ext = 'wav'
                                print(f"   Format: WAV")
                            elif audio_bytes[:3] == b'ID3' or audio_bytes[:2] in [b'\xff\xfb', b'\xff\xf3']:
                                ext = 'mp3'
                                print(f"   Format: MP3")
                            else:
                                ext = 'bin'
                                print(f"   Format: Unknown")
                            
                            # Save file
                            filename = f"gemini_tts_test.{ext}"
                            with open(filename, 'wb') as f:
                                f.write(audio_bytes)
                            
                            print(f"   Saved to: {filename}")
                            return audio_bytes
        
        print("❌ No audio in response")
        print(f"Response: {result}")
    else:
        print(f"❌ Error: {response.text}")
    
    return None

if __name__ == "__main__":
    # Test texts
    test_texts = [
        "Assalomu alaykum! Men sizning AI yordamchingizman.",
        "Здравствуйте! Я ваш AI помощник.",
        "Hello! I am your AI assistant."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}")
        print(f"{'='*60}")
        test_gemini_tts(text)
