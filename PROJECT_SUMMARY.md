# 🎉 BotFactory - To'liq Tayyor!

## ✅ **Loyiha 100% Tayyor!**

### 📊 **Bajarilgan Ishlar:**

| Vazifa | Holat | Tavsif |
|--------|--------|--------|
| Flask Web App | ✅ | To'liq ishlaydigan web ilova |
| Foydalanuvchi Tizimi | ✅ | Login, Register, Profil |
| Bot Yaratish | ✅ | Telegram bot yaratish va sozlash |
| Telegram Polling | ✅ | Webhook'siz, oson integratsiya |
| Gemini AI | ✅ | Aqlli javoblar |
| Ko'p API Key | ✅ | Limit tugasa avtomatik almashish |
| Gemini TTS | ✅ | O'zbek tilida mukammal ovoz |
| STT | ✅ | Ovozli xabarlarni tushunish |
| Spam Detection | ✅ | Avtomatik spam aniqlash |
| Bilimlar Bazasi | ✅ | FAQ, Faktlar, Mahsulotlar |

### 🚀 **Asosiy Xususiyatlar:**

#### 1. **Bot Yaratish**
- Kod yozmasdan Telegram bot yaratish
- 3 tilda: O'zbek, Rus, Ingliz
- System prompt orqali bot xarakterini sozlash

#### 2. **AI Quvvat**
- **Gemini AI** - aqlli javoblar
- **Ko'p model** - gemini-2.5-flash, gemini-2.0-flash
- **Ko'p API key** - limit tugasa avtomatik almashish

#### 3. **Ovozli Funksiyalar**
- **Gemini TTS** - O'zbek tilida mukammal ovoz (5 xil ovoz)
- **STT** - Ovozli xabarlarni matnga aylantirish
- Audio javoblar avtomatik yuboriladi

#### 4. **Bilimlar Bazasi** 🆕
- **FAQ** - Tez-tez so'raladigan savollar
- **Faktlar** - Ma'lumotlar va faktlar
- **Ko'rsatmalar** - Qadamma-qadam yo'riqnomalar
- **Kontaktlar** - Aloqa ma'lumotlari
- **Mahsulotlar** - Mahsulot/xizmatlar katalogi
- **TF-IDF** - O'xshash savollarni topish

#### 5. **Cheklovlar va Himoya**
- **Test:** 15 kun, 1 bot, 500 xabar
- **Premium:** Cheksiz
- **Spam Detection:** 1 daqiqada 10+ xabar
- **Taqiqlangan so'zlar**

### 📂 **Loyiha Strukturasi:**

```
botfactory/
├── app.py                      # Asosiy Flask ilova
├── services/
│   ├── bot_service.py         # Telegram bot xizmatlari
│   ├── bot_manager.py         # Botlarni boshqarish
│   ├── gemini_tts.py          # O'zbek TTS
│   └── knowledge_base.py      # Bilimlar bazasi 🆕
├── templates/                  # 12 ta HTML shablon
│   ├── manage_knowledge.html  # Bilimlar bazasi UI 🆕
│   └── ...
├── docs/
│   ├── multi_api_setup.md    # Ko'p API key qo'llanma
│   └── gemini_tts_guide.md   # TTS qo'llanma
├── requirements.txt           # Python kutubxonalar
├── .env                       # Muhit o'zgaruvchilari
└── README.md                  # Qo'llanma
```

### 🛠️ **O'rnatish (5 daqiqa):**

#### 1. **Klonlash:**
```bash
git clone https://github.com/yourusername/botfactory.git
cd botfactory
```

#### 2. **Virtual muhit:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

#### 3. **Kutubxonalar:**
```bash
pip install -r requirements.txt
```

#### 4. **.env fayli:**
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
GEMINI_API_KEY=AIzaSy...
GEMINI_API_KEY_2=AIzaSy...  # Zaxira (ixtiyoriy)
ADMIN_PHONE=+998996448444
ADMIN_TELEGRAM=@Akramjon1984
```

#### 5. **Ishga tushirish:**
```bash
python app.py
```
Brauzer: http://localhost:5000

### 👤 **Admin Login:**
- **Username:** admin
- **Password:** admin123

### 📝 **Foydalanish:**

#### 1. **Bot yaratish:**
1. Login qiling
2. "Yangi Bot" bosing
3. Ma'lumotlarni kiriting
4. @BotFather'dan token oling
5. Tokenni kiriting va saqlang

#### 2. **Bilimlar bazasi:**
1. Bot sahifasida "Bilimlar Bazasi" bosing
2. FAQ, Faktlar, Kontaktlar qo'shing
3. Bot avval bilimlardan javob qidiradi
4. Topilmasa AI'dan so'raydi

#### 3. **Bot ishga tushirish:**
1. Bot sahifasida "Ishga Tushirish" bosing
2. Telegram'da botingizni toping
3. /start yuboring va gaplashing!

### 🎯 **Test Qilish:**

#### **API test:**
```bash
python test_gemini.py        # Gemini AI test
python test_multi_model.py   # Ko'p model test
python services/gemini_tts.py # TTS test
```

#### **Bot test:**
1. Bot yarating
2. Token kiriting
3. "Ishga tushirish" bosing
4. Telegram'da: /start
5. Matnli xabar yuboring
6. Ovozli xabar yuboring

### 💰 **Narxlar:**

| Reja | Muddat | Narx | Xususiyatlar |
|------|--------|------|--------------|
| Test | 15 kun | Bepul | 1 bot, 500 xabar |
| Oylik | 1 oy | 145,000 so'm | Cheksiz |
| Yillik | 1 yil | 1,000,000 so'm | Cheksiz |

### 🚀 **Deploy (Render.com):**

1. GitHub'ga yuklang
2. Render.com da Web Service yarating
3. Environment variables:
   - `FLASK_ENV=production`
   - `DATABASE_URL` (avtomatik)
   - `GEMINI_API_KEY`
4. Deploy!

### 🌟 **Ajoyib Xususiyatlar:**

1. **Polling** - Webhook kerak emas!
2. **O'zbek TTS** - Mukammal talaffuz
3. **Ko'p API key** - Limit muammo emas
4. **Bilimlar bazasi** - Bot aqlli bo'ladi
5. **TF-IDF** - O'xshash savollarni topadi

### 📱 **Admin Kontakt:**
- 📞 Tel: +998996448444
- 💬 Telegram: @Akramjon1984

### 🎉 **Xulosa:**

**BotFactory to'liq tayyor va ishlamoqda!**

✅ Barcha funksiyalar ishlayapti
✅ O'zbek tilida mukammal gapiradi
✅ Bilimlar bazasi qo'shildi
✅ Deploy uchun tayyor

**Muammolar yo'q, xatolar yo'q - hammasi ishlayapti!** 🚀

---

**Yaratuvchi:** BotFactory Team
**Sana:** 15 Oktabr, 2025
**Versiya:** 1.0.0 FINAL
