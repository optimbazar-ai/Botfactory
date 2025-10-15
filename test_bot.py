import asyncio
from app import create_app, db
from app.models.bot import Bot
from telegram import Bot as TelegramBot

async def test_bot_connection(bot_id):
    """Test bot configuration and connectivity"""
    app = create_app()
    app.app_context().push()
    
    bot = Bot.query.get(bot_id)
    if not bot:
        print(f"❌ Bot #{bot_id} topilmadi!")
        return
    
    print(f"\n{'='*60}")
    print(f"Bot: {bot.name}")
    print(f"{'='*60}")
    
    # 1. Check Telegram token
    print("\n1️⃣ Telegram Token tekshiruvi:")
    if not bot.telegram_token:
        print("   ❌ Token yo'q!")
        return
    
    try:
        telegram_bot = TelegramBot(token=bot.telegram_token)
        me = await telegram_bot.get_me()
        print(f"   ✅ Token to'g'ri: @{me.username}")
        print(f"   Bot ID: {me.id}")
    except Exception as e:
        print(f"   ❌ Token xato: {str(e)}")
        return
    
    # 2. Check webhook status
    print("\n2️⃣ Webhook holati:")
    try:
        webhook_info = await telegram_bot.get_webhook_info()
        if webhook_info.url:
            print(f"   ✅ Webhook o'rnatilgan: {webhook_info.url}")
            print(f"   Kutilayotgan xabarlar: {webhook_info.pending_update_count}")
            if webhook_info.last_error_message:
                print(f"   ⚠️  Oxirgi xato: {webhook_info.last_error_message}")
        else:
            print("   ⚠️  Webhook o'rnatilmagan!")
            print("   💡 Webhookni o'rnatish uchun:")
            print(f"      http://localhost:5000/telegram/setup/{bot.id}")
    except Exception as e:
        print(f"   ❌ Xato: {str(e)}")
    
    # 3. Check AI configuration
    print("\n3️⃣ AI konfiguratsiyasi:")
    from config import Config
    if Config.GOOGLE_API_KEY:
        print("   ✅ Google API Key o'rnatilgan")
    else:
        print("   ❌ Google API Key yo'q!")
    
    if bot.system_prompt:
        print(f"   ✅ System Prompt: {bot.system_prompt[:50]}...")
    else:
        print("   ⚠️  System Prompt yo'q (standart javob beradi)")
    
    # 4. Check knowledge base
    print("\n4️⃣ Knowledge Base:")
    kb_count = bot.knowledge_bases.count()
    if kb_count > 0:
        print(f"   ✅ {kb_count} ta fayl yuklangan")
        for kb in bot.knowledge_bases:
            print(f"      - {kb.filename} ({kb.file_size} bytes)")
    else:
        print("   ℹ️  Knowledge Base fayllar yo'q")
    
    # 5. Test message
    print("\n5️⃣ Test xabar yuborish:")
    print("   Local testdan foydalaning:")
    print(f"   http://localhost:5000/telegram/test/{bot.id}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Foydalanish: python test_bot.py <bot_id>")
        print("Masalan: python test_bot.py 1")
        sys.exit(1)
    
    bot_id = int(sys.argv[1])
    asyncio.run(test_bot_connection(bot_id))
