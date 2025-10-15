from app import create_app
from app.services.ai_service import get_gemini_response, test_gemini_connection
from app.models.bot import Bot

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Google Gemini AI Test")
    print("=" * 60)
    
    # Test 1: Check API connection
    print("\n1. API Connection testi:")
    if test_gemini_connection():
        print("   ✅ Google API Key ishlayapti!")
    else:
        print("   ❌ Google API Key xato!")
        exit(1)
    
    # Test 2: Simple message
    print("\n2. Oddiy xabar testi:")
    try:
        response = get_gemini_response("Salom", language="uz")
        print(f"   Javob: {response}")
    except Exception as e:
        print(f"   ❌ Xatolik: {str(e)}")
    
    # Test 3: Bot 2 with knowledge base
    print("\n3. Bot 2 (akr) - Knowledge Base bilan test:")
    bot = Bot.query.get(2)
    if bot:
        from app.services.kb_service import combine_knowledge_bases
        knowledge_bases = bot.knowledge_bases.all()
        kb_text = combine_knowledge_bases(knowledge_bases) if knowledge_bases else None
        
        print(f"   Bot: {bot.name}")
        print(f"   System Prompt: {'Bor' if bot.system_prompt else 'Yoq'}")
        print(f"   Knowledge Base: {len(kb_text) if kb_text else 0} belgili")
        
        try:
            test_message = "Optombazar haqida ma'lumot ber"
            print(f"\n   Test xabar: '{test_message}'")
            
            response = get_gemini_response(
                user_message=test_message,
                system_prompt=bot.system_prompt,
                language=bot.language,
                knowledge_base_text=kb_text
            )
            print(f"\n   ✅ Javob olindi:")
            print(f"   {response[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Xatolik: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
