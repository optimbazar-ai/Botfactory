"""
Mavjud Gemini modellarini ko'rish
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env faylini yuklash
load_dotenv()

# API key olish
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY .env faylida yo'q!")
    exit(1)

# Gemini'ni sozlash
genai.configure(api_key=api_key)

print("📋 Mavjud Gemini modellari:\n")

# Modellarni ko'rish
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Tavsif: {model.display_name}")
        print(f"   Methods: {', '.join(model.supported_generation_methods)}")
        print()

print("\n💡 Tavsiya: 'gemini-1.5-flash' yoki 'gemini-1.5-pro' modellarini ishlating!")
