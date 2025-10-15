"""
Bot yaratish va monitoring test
"""
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

async def test_bot_token():
    """Bot token tekshirish"""
    # Rasmdagi tokenni test qilish
    token = "123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Shu yerni to'g'ri token bilan almashtiring
    
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Bot ishlayapti!")
        print(f"   Username: @{me.username}")
        print(f"   Bot nomi: {me.first_name}")
        print(f"   Bot ID: {me.id}")
        return True
    except Exception as e:
        print(f"❌ Bot token noto'g'ri yoki bot ishlamayapti!")
        print(f"   Xatolik: {e}")
        return False

async def test_chat_id():
    """Chat ID tekshirish"""
    chat_id = "123456789"  # Rasmdagi chat ID
    
    # Test uchun bot token kerak
    token = os.getenv('TEST_BOT_TOKEN')
    if not token:
        print("⚠️ TEST_BOT_TOKEN muhit o'zgaruvchisini .env faylida o'rnating")
        return
    
    try:
        bot = Bot(token=token)
        await bot.send_message(
            chat_id=chat_id,
            text="✅ Suhbat kuzatuvi test xabari!\n\nAgar bu xabarni ko'rayotgan bo'lsangiz, monitoring ishlayapti!"
        )
        print(f"✅ Chat ID to'g'ri, xabar yuborildi!")
        return True
    except Exception as e:
        print(f"❌ Chat ID noto'g'ri yoki bot admin emas!")
        print(f"   Xatolik: {e}")
        return False

async def main():
    print("🔍 BOT VA MONITORING TEST")
    print("=" * 50)
    
    print("\n1️⃣ BOT TOKEN TEST:")
    print("   Rasmdagi token bilan test qilish...")
    await test_bot_token()
    
    print("\n2️⃣ CHAT ID TEST:")
    print("   Admin chat ID test...")
    await test_chat_id()
    
    print("\n" + "=" * 50)
    print("💡 TAVSIYALAR:")
    print("1. @BotFather'ga boring va yangi bot yarating")
    print("2. Olingan tokenni 'Telegram Bot Token' maydoniga kiriting")
    print("3. @userinfobot'ga yozing va /start bosing")
    print("4. Olingan chat ID ni 'Admin Chat ID' maydoniga kiriting")
    print("5. Bot yaratgandan keyin 'Ishga tushirish' tugmasini bosing!")

if __name__ == "__main__":
    asyncio.run(main())
