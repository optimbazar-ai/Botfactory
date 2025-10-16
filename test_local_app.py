#!/usr/bin/env python
"""
Local test - app'ni ishga tushirish va bot manager tekshirish
"""
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

print(f"{Fore.CYAN}🚀 BOTFACTORY LOCAL TEST{Style.RESET_ALL}")
print("="*50)

# Environment variables tekshirish
print(f"\n{Fore.YELLOW}📋 Environment Variables:{Style.RESET_ALL}")
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"{Fore.GREEN}✅ GEMINI_API_KEY: {gemini_key[:10]}...{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}❌ GEMINI_API_KEY: NOT SET{Style.RESET_ALL}")

openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print(f"{Fore.GREEN}✅ OPENAI_API_KEY: {openai_key[:10]}...{Style.RESET_ALL}")
else:
    print(f"{Fore.YELLOW}⚠️ OPENAI_API_KEY: NOT SET (optional){Style.RESET_ALL}")

# App'ni ishga tushirish
print(f"\n{Fore.YELLOW}🔧 App'ni ishga tushirish...{Style.RESET_ALL}")

try:
    from app import app, bot_manager, db
    
    with app.app_context():
        # Database test
        db.session.execute(db.text('SELECT 1'))
        print(f"{Fore.GREEN}✅ Database ulandi{Style.RESET_ALL}")
        
        # Bot manager test
        if bot_manager:
            print(f"{Fore.GREEN}✅ Bot Manager mavjud{Style.RESET_ALL}")
            running = bot_manager.get_all_running_bots()
            print(f"{Fore.CYAN}   Ishlayotgan botlar: {len(running)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Bot Manager yo'q!{Style.RESET_ALL}")
            
        # Flask test client
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Flask app ishlayapti (/ = 200 OK){Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Flask app muammo (/ = {response.status_code}){Style.RESET_ALL}")
                
        print(f"\n{Fore.GREEN}🎉 LOCAL TEST MUVAFFAQIYATLI!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📍 Endi app'ni ishga tushiring:{Style.RESET_ALL}")
        print(f"   python app.py")
        print(f"   yoki")
        print(f"   flask run")
        
except Exception as e:
    print(f"{Fore.RED}❌ XATOLIK: {e}{Style.RESET_ALL}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
