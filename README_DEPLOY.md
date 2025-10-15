# 🚀 BotFactory - Tezkor Deploy Qo'llanmasi

## ⚡ 5 DAQIQADA DEPLOY!

### 1️⃣ GitHub'ga yuklash (2 min)

```bash
git init
git add .
git commit -m "BotFactory deploy ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/botfactory.git
git push -u origin main
```

### 2️⃣ Render.com (3 min)

1. **Render.com**'ga kiring: https://render.com
2. **New PostgreSQL** yarating:
   - Name: `botfactory-db`
   - Plan: Free
   - **Create** bosing
   - **Internal Database URL**ni kochiring

3. **New Web Service** yarating:
   - GitHub repo'ni ulang
   - Name: `botfactory`
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `bash start.sh`
   - Plan: Free

4. **Environment Variables** qo'shing:
   ```
   SECRET_KEY = [auto-generated]
   FLASK_ENV = production
   DATABASE_URL = [PostgreSQL URL]
   GEMINI_API_KEY = [your-key]
   ADMIN_PASSWORD = [secure-password]
   ```

5. **Create Web Service** bosing

### 3️⃣ TAYYOR! ✅

```
https://botfactory-xxxxx.onrender.com
```

Login: **admin** / **[ADMIN_PASSWORD]**

---

## 📋 Kerakli API Keys

### Gemini API Key:
1. https://makersuite.google.com/app/apikey ga o'ting
2. **Create API Key** bosing
3. Key'ni kochiring

### OpenAI API Key (optional):
1. https://platform.openai.com/api-keys ga o'ting
2. **Create new secret key** bosing
3. Key'ni kochiring

---

## 🔥 Tez-tez so'raladigan savollar

### Q: Deploy qancha vaqt oladi?
**A:** 5-10 daqiqa

### Q: Narxi qancha?
**A:** **BEPUL!** Render.com free plan

### Q: Database limiti?
**A:** 1 GB (1000+ bot uchun yetarli)

### Q: Bot uxlab qoladimi?
**A:** Ha, 15 daqiqa faoliyatsizlikdan keyin. **UptimeRobot** bilan oldini oling.

### Q: Custom domain?
**A:** Render.com'da sozlash mumkin

---

## 🛠️ Monitoring

### UptimeRobot sozlash:

1. https://uptimerobot.com ga o'ting
2. **Add New Monitor** bosing
3. URL: `https://botfactory-xxxxx.onrender.com/health`
4. Interval: 10 minutes
5. **Create Monitor** bosing

---

## 📞 Yordam

**Telegram:** @Akramjon1984
**Email:** support@botfactory.uz

**To'liq qo'llanma:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

**BotFactory - Professional Telegram Bot Platform** 🤖
