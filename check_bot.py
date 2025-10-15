"""
Bot holatini to'liq tekshirish
"""
import sqlite3
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

def check_database():
    """Database'da botlar mavjudligini tekshirish"""
    print("\n📊 DATABASE TEKSHIRISH:")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('instance/botfactory.db')
        cursor = conn.cursor()
        
        # Botlarni ko'rish
        cursor.execute("SELECT id, name, telegram_token, telegram_username, is_active FROM bots")
        bots = cursor.fetchall()
        
        if not bots:
            print("❌ Hech qanday bot topilmadi!")
            print("💡 Avval bot yaratishingiz kerak:")
            print("   1. http://localhost:5000 ga kiring")
            print("   2. 'Yangi Bot Yaratish' bosing")
            return None
        
        print(f"✅ {len(bots)} ta bot topildi:\n")
        
        for bot in bots:
            bot_id, name, token, username, is_active = bot
            print(f"Bot #{bot_id}: {name}")
            print(f"  Username: @{username if username else 'nomalum'}")
            print(f"  Token: {'***' + token[-10:] if token else 'YOQ'}")
            print(f"  Status: {'✅ FAOL' if is_active else '❌ NOFAOL'}")
            print()
        
        conn.close()
        return bots[0] if bots else None
        
    except Exception as e:
        print(f"❌ Database xatolik: {e}")
        return None

async def check_telegram_bot(token):
    """Telegram bot token tekshirish"""
    print("\n🤖 TELEGRAM BOT TEKSHIRISH:")
    print("=" * 50)
    
    if not token:
        print("❌ Token mavjud emas!")
        return False
    
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Bot ishlayapti!")
        print(f"   Username: @{me.username}")
        print(f"   Bot nomi: {me.first_name}")
        print(f"   Bot ID: {me.id}")
        
        # Webhook tekshirish
        webhook = await bot.get_webhook_info()
        if webhook.url:
            print(f"⚠️ Webhook o'rnatilgan: {webhook.url}")
            print("   Polling ishlamaydi, webhook o'chirilishi kerak!")
            # Webhook o'chirish
            await bot.delete_webhook()
            print("✅ Webhook o'chirildi!")
        else:
            print("✅ Webhook yo'q, polling ishlashi mumkin")
            
        return True
    except Exception as e:
        print(f"❌ Bot token xatolik: {e}")
        print("\n💡 YECHIM:")
        print("1. @BotFather'ga o'ting")
        print("2. /mybots yuboring")
        print("3. Botingizni tanlang")
        print("4. 'API Token' ni bosing")
        print("5. Yangi token oling va BotFactory'da yangilang")
        return False

def check_bot_manager():
    """Bot Manager holatini tekshirish"""
    print("\n⚙️ BOT MANAGER TEKSHIRISH:")
    print("=" * 50)
    
    # Flask app ishlayaptimi?
    import requests
    try:
        response = requests.get("http://localhost:5000", timeout=2)
        if response.status_code == 200:
            print("✅ Flask app ishlayapti")
        else:
            print(f"⚠️ Flask app javob berdi: {response.status_code}")
    except:
        print("❌ Flask app ishlamayapti!")
        print("💡 Terminal'da: python app.py")
        return False
    
    return True

async def main():
    print("🔍 BOT DIAGNOSTIKA")
    print("=" * 50)
    
    # 1. Database tekshirish
    bot = check_database()
    
    if not bot:
        return
    
    # 2. Token tekshirish
    bot_id, name, token, username, is_active = bot
    
    if token:
        await check_telegram_bot(token)
    else:
        print("\n❌ Bot token yo'q!")
        print("💡 BotFactory'da bot tahrirlang va token kiriting")
    
    # 3. Bot Manager tekshirish
    check_bot_manager()
    
    # 4. Status tekshirish
    print("\n📊 XULOSA:")
    print("=" * 50)
    
    if not is_active:
        print("❌ BOT NOFAOL!")
        print("\n💡 YECHIM:")
        print("1. http://localhost:5000 ga kiring")
        print("2. Bot sahifasiga o'ting")
        print("3. 'Ishga Tushirish' tugmasini bosing")
        print("4. Status 'Faol' bo'lishi kerak")
    else:
        print("✅ Bot faol, lekin muammo bor bo'lishi mumkin")
        print("\n💡 TAVSIYALAR:")
        print("1. Flask app'ni qayta ishga tushiring (Ctrl+C, python app.py)")
        print("2. Bot sahifasida To'xtatish keyin Ishga Tushirish bosing")
        print("3. Yangi token oling @BotFather'dan")
    
    print("\n📱 TELEGRAM'DA TEST:")
    print("=" * 50)
    if username:
        print(f"1. Telegram'da @{username} ni toping")
        print("2. 'Start' tugmasini bosing yoki /start yuboring")
        print("3. Agar javob kelmasa, yuqoridagi yechimlarni qo'llang")
    else:
        print("Bot username nomalum, token yangilash kerak")

if __name__ == "__main__":
    asyncio.run(main())
