"""
Test Gemini audio transcription with a sample file
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# Configure API
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Use the audio file we created earlier
audio_file_path = "test_audio_uz.mp3"

if not os.path.exists(audio_file_path):
    print(f"❌ Audio file not found: {audio_file_path}")
    exit(1)

print(f"📤 Uploading audio file: {audio_file_path}")

try:
    # Upload file
    uploaded_file = genai.upload_file(audio_file_path)
    print(f"✅ File uploaded: {uploaded_file.name}")
    print(f"   State: {uploaded_file.state.name}")
    
    # Wait for processing
    print(f"⏳ Waiting for processing...")
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(1)
        uploaded_file = genai.get_file(uploaded_file.name)
        print(f"   State: {uploaded_file.state.name}")
    
    if uploaded_file.state.name == "FAILED":
        print(f"❌ File processing failed!")
        exit(1)
    
    print(f"✅ File ready: {uploaded_file.state.name}")
    
    # Try transcription
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = "Bu ovozli xabardagi gapni faqat o'zbek tilida yozing. Aytilgan so'zlarni aniq yozing:"
    
    print(f"\n🔄 Transcribing...")
    response = model.generate_content([prompt, uploaded_file])
    
    if response and response.text:
        print(f"\n✅ Transcription successful!")
        print(f"📝 Text: {response.text}")
    else:
        print(f"\n❌ No text in response")
        print(f"Response: {response}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
