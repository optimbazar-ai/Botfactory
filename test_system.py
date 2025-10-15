"""
Loyiha to'liq test - barcha qismlarni tekshirish
"""
import sys
import os

print("🔍 LOYIHA TEKSHIRUVI BOSHLANDI")
print("=" * 50)

# 1. Import test
errors = []
warnings = []

print("\n1️⃣ IMPORT TEST:")
modules_to_test = [
    ("Flask", "flask"),
    ("SQLAlchemy", "flask_sqlalchemy"),
    ("Flask-Login", "flask_login"),
    ("Telegram Bot", "telegram"),
    ("Gemini AI", "google.generativeai"),
    ("Speech Recognition", "speech_recognition"),
    ("gTTS", "gtts"),
    ("PyDub", "pydub"),
    ("Scikit-learn", "sklearn"),
    ("NumPy", "numpy"),
    ("Requests", "requests"),
    ("Bcrypt", "bcrypt"),
    ("Dotenv", "dotenv")
]

for name, module in modules_to_test:
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError as e:
        print(f"  ❌ {name}: {e}")
        errors.append(f"{name} import xatolik")

# 2. File system test
print("\n2️⃣ FAYL TIZIMI TEST:")
required_dirs = [
    "templates",
    "services", 
    "docs",
    "knowledge",
    "instance"
]

for dir_name in required_dirs:
    if os.path.exists(dir_name):
        file_count = len([f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))])
        print(f"  ✅ {dir_name}/ - {file_count} ta fayl")
    else:
        print(f"  ⚠️ {dir_name}/ - mavjud emas")
        warnings.append(f"{dir_name} papka yo'q")

# 3. Service files test
print("\n3️⃣ SERVICE FAYLLAR TEST:")
service_files = [
    ("Bot Service", "services/bot_service.py"),
    ("Bot Manager", "services/bot_manager.py"),
    ("Gemini TTS", "services/gemini_tts.py"),
    ("Knowledge Base", "services/knowledge_base.py")
]

for name, file_path in service_files:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"  ✅ {name} - {size/1024:.1f} KB")
    else:
        print(f"  ❌ {name} - topilmadi")
        errors.append(f"{name} fayl yo'q")

# 4. Template files test
print("\n4️⃣ TEMPLATE FAYLLAR TEST:")
template_files = [
    "base.html",
    "index.html",
    "login.html",
    "register.html",
    "dashboard.html",
    "create_bot.html",
    "view_bot.html",
    "edit_bot_modern.html",
    "manage_knowledge.html"
]

for template in template_files:
    template_path = f"templates/{template}"
    if os.path.exists(template_path):
        print(f"  ✅ {template}")
    else:
        print(f"  ❌ {template} - topilmadi")
        errors.append(f"{template} shablon yo'q")

# 5. Environment test
print("\n5️⃣ MUHIT O'ZGARUVCHILARI TEST:")
env_vars = [
    "FLASK_ENV",
    "SECRET_KEY",
    "GEMINI_API_KEY"
]

from dotenv import load_dotenv
load_dotenv()

for var in env_vars:
    value = os.getenv(var)
    if value:
        if "KEY" in var:
            print(f"  ✅ {var} = ***")
        else:
            print(f"  ✅ {var} = {value}")
    else:
        print(f"  ⚠️ {var} - o'rnatilmagan")
        warnings.append(f"{var} muhit o'zgaruvchisi yo'q")

# 6. Database test
print("\n6️⃣ DATABASE TEST:")
db_path = "instance/botfactory.db"
if os.path.exists(db_path):
    size = os.path.getsize(db_path) / 1024
    print(f"  ✅ Database mavjud - {size:.1f} KB")
    
    # Table test
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"  ✅ Jadvallar soni: {len(tables)}")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"     - {table[0]}: {count} ta yozuv")
        conn.close()
    except Exception as e:
        print(f"  ❌ Database xatolik: {e}")
        errors.append("Database muammo")
else:
    print(f"  ⚠️ Database topilmadi")
    warnings.append("Database yo'q")

# 7. Test scripts
print("\n7️⃣ TEST SKRIPTLAR:")
test_scripts = [
    "test_gemini.py",
    "test_multi_model.py",
    "test_simple.py",
    "list_models.py"
]

for script in test_scripts:
    if os.path.exists(script):
        print(f"  ✅ {script}")
    else:
        print(f"  ⚠️ {script} - yo'q")

# NATIJA
print("\n" + "=" * 50)
print("📊 TEKSHIRUV NATIJALARI:")

if not errors and not warnings:
    print("✅ ✅ ✅ LOYIHA TO'LIQ TAYYOR! ✅ ✅ ✅")
    print("Barcha komponentlar ishlayapti!")
else:
    if errors:
        print(f"\n❌ XATOLIKLAR ({len(errors)} ta):")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print(f"\n⚠️ OGOHLANTIRISHLAR ({len(warnings)} ta):")
        for warning in warnings:
            print(f"   - {warning}")
    
    print("\n💡 TAVSIYALAR:")
    if any("import" in e for e in errors):
        print("   - pip install -r requirements.txt")
    if any("papka" in w for w in warnings):
        print("   - Kerakli papkalarni yarating")
    if any("muhit" in w for w in warnings):
        print("   - .env faylini tekshiring")

# Web app holati
print("\n🌐 WEB APP HOLATI:")
import requests
try:
    response = requests.get("http://localhost:5000", timeout=2)
    if response.status_code == 200:
        print("  ✅ Flask app ishlayapti - http://localhost:5000")
    else:
        print(f"  ⚠️ Flask app javob berdi lekin status: {response.status_code}")
except:
    print("  ❌ Flask app ishlamayapti yoki localhost:5000 band")

print("\n✨ Test yakunlandi!")
