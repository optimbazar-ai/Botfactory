"""
Callback handler test
"""
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

async def test_callback():
    """Test til tanlash tugmalari"""
    token = "7568964660:AAHx_cinhFhE9yo-iBmyJKjikr7iQYA8VgY"
    chat_id = "1021369075"  # Admin chat ID
    
    try:
        bot = Bot(token=token)
        
        # Til tanlash tugmalari
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
            ],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Test xabar yuborish
        message = await bot.send_message(
            chat_id=chat_id,
            text="👋 Test: Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=reply_markup
        )
        
        print("✅ Test xabar yuborildi!")
        print(f"   Message ID: {message.message_id}")
        print(f"   Chat ID: {chat_id}")
        print("\n📱 Telegram'da tugmani bosing va natijani kuzating!")
        print("\nAgar tugma ishlamasa:")
        print("1. Bot to'xtatilgan bo'lishi mumkin")
        print("2. CallbackQueryHandler qo'shilmagan")
        print("3. Flask app'ni qayta ishga tushiring")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(test_callback())
