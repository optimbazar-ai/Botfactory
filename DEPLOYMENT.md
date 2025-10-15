# 🚀 BotFactory - Render.com Deploy Qo'llanmasi

## 📋 Talab qilingan narsalar

- GitHub account
- Render.com account (bepul)
- Gemini API key (https://makersuite.google.com/app/apikey)

## 🔥 1-QADAM: GitHub'ga yuklash

### Git repository yaratish:

```bash
cd e:\loyihalarim\botfactory

# Git init
git init

# Barcha fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Initial commit - BotFactory ready for deployment"

# GitHub'ga push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/botfactory.git
git push -u origin main
```

## 🌐 2-QADAM: Render.com'da deploy qilish

### A. Render.com'ga kirish:

1. https://render.com ga o'ting
2. **Sign Up** yoki **Login** qiling
3. GitHub account bilan bog'lang

### B. PostgreSQL Database yaratish:

1. **Dashboard** -> **New** -> **PostgreSQL**
2. Settings:
   - **Name:** `botfactory-db`
   - **Database:** `botfactory`
   - **User:** `botfactory_user`
   - **Region:** Frankfurt (yaqinroq)
   - **Plan:** Free
3. **Create Database** bosing
4. **Internal Database URL**ni kochiring

### C. Web Service yaratish:

1. **Dashboard** -> **New** -> **Web Service**
2. **GitHub repository**ni tanlang
3. Settings:
   - **Name:** `botfactory`
   - **Region:** Frankfurt
   - **Branch:** `main`
   - **Root Directory:** `.` (bo'sh qoldiring)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `bash start.sh`
   - **Plan:** Free

### D. Environment Variables qo'shish:

**Environment** tab'ida quyidagilarni qo'shing:

```
SECRET_KEY = [Auto Generated - Render beradi]
FLASK_ENV = production
DATABASE_URL = [PostgreSQL URL - Database'dan kochiring]
GEMINI_API_KEY = [Sizning Gemini API key]
ADMIN_PASSWORD = [Xavfsiz parol]
ADMIN_PHONE = +998996448444
```

### E. Deploy qiling:

1. **Create Web Service** bosing
2. Deploy jarayoni 5-10 daqiqa davom etadi
3. Logs'ni kuzating

## ✅ 3-QADAM: Deploy muvaffaqiyatli!

### Sizning URL:

```
https://botfactory-xxxxx.onrender.com
```

### Login ma'lumotlari:

```
Username: admin
Password: [ADMIN_PASSWORD environment variable]
```

## 🤖 4-QADAM: Telegram Bot'ni sozlash

### A. BotFather'da webhook o'rnatish:

```bash
# Telegram'da @BotFather ga yuboring:
/setwebhook
# Keyin URL'ni yuboring:
https://botfactory-xxxxx.onrender.com/webhook/YOUR_BOT_TOKEN
```

### B. Yoki web interface orqali:

1. BotFactory'ga kiring
2. Bot yarating
3. Bot avtomatik webhook o'rnatadi

## ⚙️ 5-QADAM: Sozlamalar

### Free plan limitleri:

- **Database:** 1 GB
- **Bandwidth:** 100 GB/oy
- **Auto-sleep:** 15 daqiqa faoliyatsizlikdan keyin uxlaydi
- **Build time:** 500 soat/oy

### Auto-sleep'ni oldini olish:

Cron-job.org yoki UptimeRobot bilan 10 daqiqada bir marta ping qiling:

```
https://botfactory-xxxxx.onrender.com/health
```

### Monitoring:

Render Dashboard'da:
- **Logs** - Real-time logs
- **Metrics** - CPU/Memory usage
- **Events** - Deploy history

## 🔧 XATOLIK HAL QILISH

### 1. Database connection error:

```bash
# DATABASE_URL to'g'ri sozlanganini tekshiring
# Format: postgresql://user:password@host:5432/dbname
```

### 2. Build fails:

```bash
# requirements.txt'ni tekshiring
# Render logs'da xatolikni ko'ring
```

### 3. App crashes on start:

```bash
# Environment variables to'g'ri sozlanganini tekshiring
# GEMINI_API_KEY majburiy!
```

### 4. Bot javob bermayapti:

```bash
# Webhook URL to'g'rimi?
# Bot token to'g'rimi?
# Render app uxlab qolganmi? (15 daqiqa faoliyatsizlik)
```

## 📊 DATABASE BACKUP

### PostgreSQL backup:

Render Dashboard -> Database -> **Backups** tab

### Qo'lda backup:

```bash
# Render CLI orqali
render pg:backup botfactory-db
```

## 🔄 YANGILANISH

### Kod yangilanganda:

```bash
git add .
git commit -m "Update description"
git push

# Render avtomatik yangi deploy qiladi
```

### Manual deploy:

Render Dashboard -> **Manual Deploy** -> **Deploy latest commit**

## 📱 TELEGRAM BOT SOZLASH

### Webhook o'rnatish:

```
POST https://api.telegram.org/bot<TOKEN>/setWebhook
Body: {"url": "https://botfactory-xxxxx.onrender.com/webhook/<TOKEN>"}
```

### Webhook tekshirish:

```
GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

## 🎉 TAYYOR!

Sizning BotFactory platformangiz cloud'da ishlayapti!

**URL:** https://botfactory-xxxxx.onrender.com
**Admin:** username=admin, password=[ADMIN_PASSWORD]

### Keyingi qadamlar:

1. ✅ Birinchi bot yaratish
2. ✅ Bilim bazasini to'ldirish
3. ✅ Foydalanuvchilarni ro'yxatdan o'tkazish
4. ✅ Monitoring o'rnatish

**Muvaffaqiyat!** 🚀

---

## 📞 Yordam

**Muammolar?**
- Render docs: https://render.com/docs
- Telegram: @Akramjon1984
- GitHub Issues: https://github.com/YOUR_USERNAME/botfactory/issues

**BotFactory - Professional Telegram Bot Platform** 🤖
