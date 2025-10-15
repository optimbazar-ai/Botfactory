"""
Tez bot yaratish uchun script
"""
import sqlite3
import bcrypt
from datetime import datetime, timedelta

def create_test_bot():
    """Test bot yaratish"""
    print("🤖 TEST BOT YARATISH")
    print("=" * 50)
    
    # Ma'lumotlarni so'rash
    print("\n📝 Bot ma'lumotlarini kiriting:\n")
    
    bot_name = input("Bot nomi (masalan: Test Bot): ").strip()
    if not bot_name:
        bot_name = "Test Bot"
    
    bot_token = input("Telegram Bot Token (@BotFather'dan): ").strip()
    if not bot_token:
        print("❌ Token majburiy!")
        print("\n💡 Qanday olish:")
        print("1. @BotFather'ga o'ting")
        print("2. /newbot yuboring")
        print("3. Bot nomi va username kiriting")
        print("4. Tokenni kochiring va qayta ishga tushiring")
        return
    
    admin_chat_id = input("Sizning Chat ID (monitoring uchun): ").strip()
    if not admin_chat_id:
        print("⚠️ Chat ID kiritilmadi, monitoring ishlamaydi")
        print("Chat ID olish: @userinfobot ga /start yuboring")
    
    # Bot username olish
    bot_username = None
    try:
        import requests
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe')
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                bot_username = bot_info['result']['username']
                print(f"✅ Bot topildi: @{bot_username}")
    except Exception as e:
        print(f"⚠️ Bot username olib bo'lmadi: {e}")
    
    # Database'ga yozish
    try:
        conn = sqlite3.connect('instance/botfactory.db')
        cursor = conn.cursor()
        
        # Admin user ID olish (birinchi user)
        cursor.execute("SELECT id FROM users LIMIT 1")
        user = cursor.fetchone()
        
        if not user:
            print("❌ Admin user topilmadi!")
            print("Avval http://localhost:5000 da ro'yxatdan o'ting")
            return
        
        user_id = user[0]
        
        # Bot qo'shish
        cursor.execute("""
            INSERT INTO bots (
                user_id, name, description, telegram_token, 
                telegram_username, language, system_prompt, 
                is_active, admin_chat_id, notifications_enabled,
                total_messages, today_messages, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            bot_name,
            "Test bot - BotFactory orqali yaratilgan",
            bot_token,
            bot_username,
            'uz',
            "Siz yordam beruvchi virtual assistentsiz. Foydalanuvchi savollariga aniq va foydali javoblar bering.",
            1,  # is_active = True
            admin_chat_id if admin_chat_id else None,
            1 if admin_chat_id else 0,  # notifications_enabled
            0,  # total_messages
            0,  # today_messages
            datetime.now()
        ))
        
        conn.commit()
        bot_id = cursor.lastrowid
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ BOT MUVAFFAQIYATLI YARATILDI!")
        print("=" * 50)
        print(f"\n📊 Bot ma'lumotlari:")
        print(f"  ID: {bot_id}")
        print(f"  Nomi: {bot_name}")
        print(f"  Username: @{bot_username}")
        print(f"  Status: ✅ FAOL")
        if admin_chat_id:
            print(f"  Monitoring: ✅ YOQILGAN")
        
        print("\n🚀 ENDI NIMA QILISH:")
        print("1. Flask app'ni qayta ishga tushiring:")
        print("   - Ctrl+C bosing")
        print("   - python app.py")
        print(f"2. Telegram'da @{bot_username} ga o'ting")
        print("3. /start yuboring")
        print("4. Bot javob berishi kerak!")
        
        if admin_chat_id:
            print(f"\n📱 Monitoring: Barcha xabarlar {admin_chat_id} ga yuboriladi")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    create_test_bot()
