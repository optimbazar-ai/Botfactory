"""
Vosk modelini yuklab olish
"""
import os
import requests
import zipfile
from tqdm import tqdm

def download_vosk_model():
    """O'zbek tili modelini yuklab olish"""
    
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-uz-0.22.zip"
    model_dir = "models"
    model_name = "vosk-model-small-uz-0.22"
    model_path = os.path.join(model_dir, model_name)
    
    # Agar model mavjud bo'lsa
    if os.path.exists(model_path):
        print(f"✅ Model allaqachon yuklab olingan: {model_path}")
        return model_path
    
    print("📥 Vosk modelini yuklab olish boshlandi...")
    print(f"URL: {model_url}")
    
    # Models papkasini yaratish
    os.makedirs(model_dir, exist_ok=True)
    
    # Zip faylni yuklab olish
    zip_path = os.path.join(model_dir, "vosk-model.zip")
    
    try:
        response = requests.get(model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        print(f"Fayl hajmi: {total_size / 1024 / 1024:.1f} MB")
        
        with open(zip_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    pbar.update(len(chunk))
        
        print("✅ Yuklab olish tugadi!")
        print("📦 Arxivni ochish...")
        
        # Zip faylni ochish
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(model_dir)
        
        # Zip faylni o'chirish
        os.remove(zip_path)
        
        print(f"✅ Model tayyor: {model_path}")
        print(f"💾 Hajm: ~45 MB (offline ishlaydi)")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("🎤 VOSK - BEPUL OFFLINE SPEECH RECOGNITION")
    print("=" * 60)
    print("\n📋 Ma'lumot:")
    print("   - O'zbek tili modeli")
    print("   - 100% BEPUL")
    print("   - Offline ishlaydi")
    print("   - Hajm: ~45 MB")
    print("\n")
    
    model_path = download_vosk_model()
    
    if model_path:
        print("\n" + "=" * 60)
        print("🎉 TAYYOR!")
        print("=" * 60)
        print("\n📍 Model joylashuvi:")
        print(f"   {os.path.abspath(model_path)}")
        print("\n🚀 Botni ishga tushiring:")
        print("   python activate_bot.py")
        print("\n💡 Endi ovozli xabarlar BEPUL taniladi!")
    else:
        print("\n❌ Model yuklab olinmadi!")
