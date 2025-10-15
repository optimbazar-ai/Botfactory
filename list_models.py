import google.generativeai as genai
from app import create_app

app = create_app()

with app.app_context():
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    
    print("Mavjud Gemini modellar:")
    print("=" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"[OK] {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100] if model.description else 'N/A'}...")
            print()
