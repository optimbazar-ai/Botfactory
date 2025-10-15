"""
VOSK test
"""
try:
    from vosk import Model, KaldiRecognizer
    print("✅ VOSK kutubxonasi o'rnatilgan!")
    
    import os
    model_path = "models/vosk-model-small-uz-0.22"
    
    if os.path.exists(model_path):
        print(f"✅ Model mavjud: {model_path}")
    else:
        print(f"❌ Model yo'q: {model_path}")
        
except ImportError as e:
    print(f"❌ VOSK o'rnatilmagan: {e}")
