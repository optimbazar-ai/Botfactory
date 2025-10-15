# 🤖 BotFactory

Telegram botlarini kod yozmasdan yarating va boshqaring!

## ✨ Xususiyatlari

- 🚀 **Oson yaratish** - Bir necha daqiqada bot yarating
- 🧠 **AI quvvat** - Google Gemini AI bilan aqlli javoblar
- 🔄 **Ko'p API Key** - Limit tugasa avtomatik boshqa key/modelga o'tish
- 🎤 **Ovozli xabarlar** - STT va TTS qo'llab-quvvatlash
- 🌐 **Ko'p tillilik** - O'zbek, Rus, Ingliz tillari
- 🛡️ **Spam himoya** - Avtomatik spam aniqlash
- 📊 **Statistika** - To'liq bot statistikasi
- 💎 **Test/Premium** - 15 kunlik bepul test

## 🚀 O'rnatish

### 1. Loyihani klonlash
```bash
git clone https://github.com/yourusername/botfactory.git
cd botfactory
```

### 2. Virtual muhit yaratish
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash
```bash
cp .env.example .env
# .env faylini tahrirlang va kerakli API kalitlarni kiriting
```

### 5. Loyihani ishga tushirish
```bash
python app.py
```

Brauzer: http://localhost:5000

## 📝 Sozlamalar

### Gemini API Key olish:
1. https://makersuite.google.com/app/apikey ga o'ting
2. "Create API Key" tugmasini bosing
3. API key ni .env fayliga qo'shing

### Ko'p API Key sozlash (Ixtiyoriy):
```env
GEMINI_API_KEY=birinchi-api-key
GEMINI_API_KEY_2=ikkinchi-api-key
```
**Afzalligi:** Birinchi key limiti tugasa, avtomatik ikkinchisiga o'tadi!

### Telegram Bot yaratish:
1. Telegram'da @BotFather ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username kiriting
4. Olingan tokenni BotFactory'da ishlatinging

## 🎯 Foydalanish

### 1. Ro'yxatdan o'tish
- Saytda ro'yxatdan o'ting
- 15 kunlik bepul test muddati boshlanadi

### 2. Bot yaratish
- Dashboard'da "Yangi Bot" tugmasini bosing
- Bot ma'lumotlarini kiriting
- Telegram bot tokenini qo'shing

### 3. Botni ishga tushirish
- Bot sahifasida "Ishga Tushirish" tugmasini bosing
- Telegram'da botingizni sinab ko'ring

## 💰 Narxlar

- **Test**: 15 kun bepul (1 bot, 500 xabar)
- **1 oylik**: 145,000 so'm
- **1 yillik**: 1,000,000 so'm

## 🛠️ Texnologiyalar

- **Backend**: Flask (Python)
- **Database**: SQLite/PostgreSQL
- **AI**: Google Gemini
- **Bot**: python-telegram-bot
- **TTS**: Google Text-to-Speech
- **STT**: Google Speech Recognition
- **Frontend**: Bootstrap 5

## 📱 Admin Aloqa

- 📞 Telefon: +998996448444
- 💬 Telegram: @Akramjon1984

## 🔧 Deployment (Render.com)

1. Render.com da yangi "Web Service" yarating
2. GitHub repo'ni ulang
3. Environment variables qo'shing:
   - `FLASK_ENV=production`
   - `DATABASE_URL` (avtomatik)
   - `GEMINI_API_KEY`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`

## 📄 Litsenziya

MIT License

## 👨‍💻 Muallif

BotFactory Team

---

**Savol va takliflar uchun admin bilan bog'laning!**
