"""
Database ni to'liq qayta yaratish
"""
import os
import shutil

# Eski database fayllarini o'chirish
if os.path.exists('instance'):
    try:
        shutil.rmtree('instance')
        print("✅ Eski instance papkasi o'chirildi")
    except:
        print("❌ Instance papkasini o'chirib bo'lmadi")

# Eski db fayllarni o'chirish        
for db_file in ['botfactory.db', 'botfactory_new.db']:
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"✅ {db_file} o'chirildi")
        except:
            print(f"❌ {db_file} o'chirib bo'lmadi")

print("✅ Database tozalandi!")
print("🚀 Endi app.py ni qayta ishga tushiring")
