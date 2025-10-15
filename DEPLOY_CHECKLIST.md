# ✅ BotFactory Deploy Checklist

## 📋 Deploy oldin tekshiring:

### 1. Kod tayyor:
- [x] `render.yaml` - Render konfiguratsiya
- [x] `start.sh` - Ishga tushirish script
- [x] `.env.production.example` - Environment variables namuna
- [x] `requirements.txt` - Barcha dependencies
- [x] `.gitignore` - Maxfiy fayllar listida
- [x] `health` endpoint - Monitoring uchun
- [x] PostgreSQL support - `postgres://` → `postgresql://`
- [x] Production mode - `debug=False`, `PORT` env var

### 2. API Keys tayyor:
- [ ] **GEMINI_API_KEY** - https://makersuite.google.com/app/apikey
- [ ] **OPENAI_API_KEY** (optional) - https://platform.openai.com/api-keys
- [ ] **SECRET_KEY** - Render auto-generate qiladi
- [ ] **ADMIN_PASSWORD** - Xavfsiz parol

### 3. GitHub tayyor:
- [ ] Repository yaratilgan
- [ ] Barcha fayllar push qilingan
- [ ] `.env` push qilinmagan (gitignore'da)

### 4. Render.com tayyor:
- [ ] Account yaratilgan
- [ ] GitHub ulangan
- [ ] PostgreSQL database yaratilgan
- [ ] Web service yaratilgan
- [ ] Environment variables sozlangan

### 5. Deploy:
- [ ] Build muvaffaqiyatli
- [ ] App running
- [ ] Health check `200 OK`
- [ ] Admin login ishlayapti
- [ ] Bot yaratish ishlayapti

### 6. Post-Deploy:
- [ ] UptimeRobot sozlangan (15 daqiqa uxlamasligi uchun)
- [ ] Custom domain ulangan (optional)
- [ ] SSL sertifikat faol (Render auto)
- [ ] Backup strategiya (Render auto-backup)

---

## 🚀 Deploy buyruqlar:

```bash
# 1. Git push
git add .
git commit -m "Ready for production deploy"
git push origin main

# 2. Render.com'da:
#    - New PostgreSQL database
#    - New Web Service
#    - Environment variables
#    - Deploy

# 3. Test:
curl https://your-app.onrender.com/health
```

---

## 🔍 Deploy keyin test:

### 1. Health Check:
```bash
curl https://your-app.onrender.com/health
# Response: {"status":"healthy","database":"connected"}
```

### 2. Homepage:
```
https://your-app.onrender.com/
```

### 3. Admin Login:
```
https://your-app.onrender.com/login
Username: admin
Password: [ADMIN_PASSWORD]
```

### 4. Bot yaratish:
```
Dashboard -> Yangi bot -> Bot ma'lumotlari -> Saqlash
```

### 5. Telegram test:
```
Telegram'da botni topish
/start yuborish
Javob kelishini kutish
```

---

## ❌ Xatoliklarni hal qilish:

### Build fails:
```
# Render logs'ni tekshiring
# requirements.txt'ni tekshiring
# Python version: 3.10
```

### Database connection error:
```
# DATABASE_URL to'g'rimi?
# PostgreSQL running?
# Connection string format:
postgresql://user:password@host:5432/database
```

### App crashes:
```
# Environment variables to'g'rimi?
# GEMINI_API_KEY kiritilganmi?
# Logs'da xatolikni toping
```

### Bot javob bermayapti:
```
# Bot token to'g'rimi?
# Webhook o'rnatilganmi?
# App uxlab qolganmi? (Health check)
```

---

## 📊 Monitoring:

### Render Dashboard:
- **Logs** - Real-time
- **Metrics** - CPU/Memory
- **Events** - Deploy history

### UptimeRobot:
- Status: UP/DOWN
- Response time
- Uptime %

### Health endpoint:
```
GET /health
Response: {"status":"healthy"}
```

---

## 🎉 DEPLOY TAYYOR!

**Next steps:**
1. ✅ Bot yaratish
2. ✅ Bilim bazasini to'ldirish
3. ✅ Telegram'da test qilish
4. ✅ Users'ga tarqatish

**Good luck!** 🚀
