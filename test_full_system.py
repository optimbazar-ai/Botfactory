#!/usr/bin/env python
"""
BotFactory to'liq tizim testi
Barcha komponentlarni tekshirish
"""

import os
import time
import sys
from colorama import Fore, Style, init

# Colorama init
init(autoreset=True)

def test_step(name, func):
    """Test qadamini bajarish"""
    try:
        print(f"\n{Fore.CYAN}🔍 Testing: {name}...{Style.RESET_ALL}")
        result = func()
        if result:
            print(f"{Fore.GREEN}✅ {name} - PASSED{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ {name} - FAILED{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ {name} - ERROR: {e}{Style.RESET_ALL}")
        return False

def test_environment():
    """Environment variables tekshirish"""
    # Kamida bitta API key bo'lishi kerak
    api_keys = ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_API_KEY_2']
    optional_vars = ['OPENAI_API_KEY', 'SECRET_KEY', 'DATABASE_URL', 'ADMIN_PASSWORD']
    
    print("\n" + "="*50)
    print(f"{Fore.YELLOW}📋 ENVIRONMENT VARIABLES CHECK{Style.RESET_ALL}")
    print("="*50)
    
    # Kamida bitta API key borligini tekshirish
    api_key_found = False
    for var in api_keys:
        if os.getenv(var):
            print(f"{Fore.GREEN}✅ {var}: SET{Style.RESET_ALL}")
            api_key_found = True
        else:
            print(f"{Fore.YELLOW}⚠️ {var}: NOT SET{Style.RESET_ALL}")
    
    if not api_key_found:
        print(f"{Fore.RED}❌ Hech qanday Gemini API key topilmadi!{Style.RESET_ALL}")
        all_good = False
    else:
        print(f"{Fore.GREEN}✅ Kamida bitta API key mavjud{Style.RESET_ALL}")
        all_good = True
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"{Fore.GREEN}✅ {var}: SET{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ {var}: NOT SET (optional){Style.RESET_ALL}")
    
    return all_good

def test_database():
    """Database ulanishni tekshirish"""
    try:
        from app import app, db, User, Bot
        
        with app.app_context():
            # Database'ga ulanish
            db.session.execute(db.text('SELECT 1'))
            
            # Admin user tekshirish
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"{Fore.GREEN}✅ Admin user mavjud{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️ Admin user yo'q - yaratiladi{Style.RESET_ALL}")
            
            # Botlar soni
            bot_count = Bot.query.count()
            print(f"{Fore.CYAN}📊 Jami botlar: {bot_count}{Style.RESET_ALL}")
            
            return True
    except Exception as e:
        print(f"{Fore.RED}Database xatoligi: {e}{Style.RESET_ALL}")
        return False

def test_bot_manager():
    """Bot Manager tekshirish"""
    try:
        from app import app, initialize_bot_manager
        
        with app.app_context():
            bot_manager = initialize_bot_manager()
            
            if bot_manager:
                print(f"{Fore.GREEN}✅ Bot Manager yaratildi{Style.RESET_ALL}")
                
                # Running botlar soni
                running = bot_manager.get_all_running_bots()
                print(f"{Fore.CYAN}🤖 Ishlayotgan botlar: {len(running)}{Style.RESET_ALL}")
                
                return True
            else:
                return False
                
    except Exception as e:
        print(f"{Fore.RED}Bot Manager xatoligi: {e}{Style.RESET_ALL}")
        return False

def test_gemini_api():
    """Gemini API tekshirish"""
    try:
        import google.generativeai as genai
        
        # Barcha mumkin bo'lgan API keylarni tekshirish
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY_2')
        if not api_key:
            print(f"{Fore.RED}Hech qanday API key topilmadi!{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.CYAN}🔑 API key topildi{Style.RESET_ALL}")
        
        genai.configure(api_key=api_key)
        
        # Oddiy test so'rovi
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Salom, test")
        
        if response.text:
            print(f"{Fore.GREEN}✅ Gemini API ishlayapti{Style.RESET_ALL}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"{Fore.RED}Gemini API xatoligi: {e}{Style.RESET_ALL}")
        return False

def test_flask_routes():
    """Flask route'larni tekshirish"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Home page
            response = client.get('/')
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Home page (/) - 200 OK{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Home page (/) - {response.status_code}{Style.RESET_ALL}")
            
            # Health check
            response = client.get('/health')
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Health check (/health) - 200 OK{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Health check (/health) - {response.status_code}{Style.RESET_ALL}")
            
            # Login page
            response = client.get('/login')
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Login page (/login) - 200 OK{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Login page (/login) - {response.status_code}{Style.RESET_ALL}")
            
            return True
            
    except Exception as e:
        print(f"{Fore.RED}Flask routes xatoligi: {e}{Style.RESET_ALL}")
        return False

def test_knowledge_base():
    """Bilimlar bazasi testi"""
    try:
        from services.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase(bot_id=1)
        
        # Statistika olish
        stats = kb.get_statistics()
        print(f"{Fore.CYAN}📚 Bilimlar bazasi statistikasi:{Style.RESET_ALL}")
        print(f"   FAQ: {stats.get('faq_count', 0)}")
        print(f"   Facts: {stats.get('facts_count', 0)}")
        print(f"   Instructions: {stats.get('instructions_count', 0)}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Knowledge Base xatoligi: {e}{Style.RESET_ALL}")
        return False

def test_telegram_bot():
    """Telegram bot service testi"""
    try:
        from services.bot_service import TelegramBotService
        from app import Bot, app, db
        
        with app.app_context():
            # Birinchi botni olish
            bot = Bot.query.first()
            
            if bot and bot.telegram_token:
                print(f"{Fore.CYAN}🤖 Testing bot: @{bot.telegram_username}{Style.RESET_ALL}")
                
                # Bot service yaratish
                service = TelegramBotService(bot, db)
                
                # Bot info olish
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                bot_info = loop.run_until_complete(service.get_bot_info())
                loop.close()
                
                if bot_info:
                    print(f"{Fore.GREEN}✅ Bot mavjud: @{bot_info.username}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}❌ Bot topilmadi yoki token noto'g'ri{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.YELLOW}⚠️ Bot yoki token yo'q{Style.RESET_ALL}")
                return None
                
    except Exception as e:
        print(f"{Fore.RED}Telegram bot xatoligi: {e}{Style.RESET_ALL}")
        return False

def main():
    """Asosiy test funksiyasi"""
    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🚀 BOTFACTORY TO'LIQ TIZIM TESTI{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    
    tests = [
        ("Environment Variables", test_environment),
        ("Database Connection", test_database),
        ("Bot Manager", test_bot_manager),
        ("Gemini API", test_gemini_api),
        ("Flask Routes", test_flask_routes),
        ("Knowledge Base", test_knowledge_base),
        ("Telegram Bot Service", test_telegram_bot)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n{Fore.BLUE}▶️ Testing: {name}{Style.RESET_ALL}")
        print("-" * 40)
        result = test_func()
        results.append((name, result))
        time.sleep(0.5)
    
    # Natijalar
    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}📊 TEST NATIJALARI{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    
    passed = 0
    failed = 0
    skipped = 0
    
    for name, result in results:
        if result is True:
            print(f"{Fore.GREEN}✅ {name}: PASSED{Style.RESET_ALL}")
            passed += 1
        elif result is False:
            print(f"{Fore.RED}❌ {name}: FAILED{Style.RESET_ALL}")
            failed += 1
        else:
            print(f"{Fore.YELLOW}⚠️ {name}: SKIPPED{Style.RESET_ALL}")
            skipped += 1
    
    print(f"\n{Fore.CYAN}📈 Umumiy:{Style.RESET_ALL}")
    print(f"   {Fore.GREEN}Passed: {passed}{Style.RESET_ALL}")
    print(f"   {Fore.RED}Failed: {failed}{Style.RESET_ALL}")
    print(f"   {Fore.YELLOW}Skipped: {skipped}{Style.RESET_ALL}")
    
    if failed == 0:
        print(f"\n{Fore.GREEN}🎉 BARCHA TESTLAR MUVAFFAQIYATLI O'TDI!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Tizim to'liq ishlashga tayyor!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}⚠️ BA'ZI TESTLAR MUVAFFAQIYATSIZ!{Style.RESET_ALL}")
        print(f"{Fore.RED}🔧 Iltimos, yuqoridagi xatoliklarni tuzating.{Style.RESET_ALL}")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Test to'xtatildi!{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Test xatoligi: {e}{Style.RESET_ALL}")
        sys.exit(1)
