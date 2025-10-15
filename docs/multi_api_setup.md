# 🔄 Ko'p API Key va Model Almashish Tizimi

## 📋 Umumiy Ma'lumot

BotFactory'da **bir nechta Gemini API key** va **model almashish** tizimi mavjud. Bu tizim quyidagi afzalliklarga ega:

1. **Limit tugaganda** - Avtomatik boshqa API key ga o'tadi
2. **Model topilmasa** - Boshqa modelga o'tadi  
3. **Xatolik bo'lsa** - Zaxira variantlarni sinab ko'radi
4. **Yuqori ishonchlilik** - Bot doim ishlashda davom etadi

## 🚀 Sozlash

### 1. Birinchi API Key (Majburiy)

`.env` faylida:
```env
GEMINI_API_KEY=AIzaSy...birinchi-key
```

### 2. Ikkinchi API Key (Ixtiyoriy)

`.env` faylida qo'shing:
```env
GEMINI_API_KEY_2=AIzaSy...ikkinchi-key
```

### 3. Ko'proq API Key Kerakmi?

`services/bot_service.py` faylida tahrirlang:
```python
self.api_keys = [
    os.getenv('GEMINI_API_KEY'),
    os.getenv('GEMINI_API_KEY_2'),
    os.getenv('GEMINI_API_KEY_3'),  # Yangi
    os.getenv('GEMINI_API_KEY_4'),  # Yangi
]
```

## 🔄 Qanday Ishlaydi?

### Model Almashish Tartibi:
1. **gemini-2.5-flash** - Eng tez model (birinchi urinish)
2. **gemini-2.0-flash** - Zaxira model 1
3. **gemini-2.5-flash-lite** - Yengil model
4. **gemini-2.5-pro** - Eng kuchli model (oxirgi variant)

### Misol:
```
1. gemini-2.5-flash + API_KEY_1 → Limit tugagan ❌
2. gemini-2.5-flash + API_KEY_2 → Ishladi ✅
```

Yoki:
```
1. gemini-2.5-flash + API_KEY_1 → Limit tugagan ❌
2. gemini-2.5-flash + API_KEY_2 → Limit tugagan ❌  
3. gemini-2.0-flash + API_KEY_1 → Ishladi ✅
```

## 📊 Test Qilish

Test skriptini ishga tushiring:
```bash
python test_multi_model.py
```

## 🎯 Afzalliklari

| Xususiyat | Ta'rif |
|-----------|--------|
| **Avtomatik almashish** | Limit tugaganda boshqa key/model |
| **Yuqori ishonchlilik** | Bot doim javob beradi |
| **Iqtisodiy** | Arzon modellardan boshlanadi |
| **Moslashuvchan** | Yangi key/model qo'shish oson |

## 💡 Maslahatlar

1. **Har oy yangi API key oling** - Bepul limitlar uchun
2. **Turli modellar ishlating** - Limitlarni taqsimlash
3. **Monitoring qiling** - Qaysi model/key ishlatilayotganini kuzating
4. **Test qiling** - `test_multi_model.py` bilan tekshiring

## 🔧 Muammolar Yechimi

### API Key ishlamayapti:
1. API key to'g'riligini tekshiring
2. Google AI Studio'da faolligini tekshiring
3. Limitni tekshiring

### Model topilmayapti:
1. `list_models.py` bilan mavjud modellarni ko'ring
2. Model nomini yangilang

### Hamma keylar tugagan:
1. Yangi API key qo'shing
2. Kutib turing (limit yangilanadi)
3. Premium API key oling

## 📝 Kod Namunasi

```python
# Bot service'da foydalanish
async def get_ai_response(self, message):
    for model_name in self.models:
        for api_key in self.api_keys:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(message)
                return response.text
            except:
                continue  # Keyingi variant
    
    return "Kechirasiz, javob bera olmayman"
```

## 🌟 Xulosa

Bu tizim bilan botingiz:
- **Doim ishlaydi** - limit tugasa ham
- **Tez javob beradi** - eng tez modeldan boshlaydi  
- **Ishonchli** - bir nechta zaxira variant

**Savol bo'lsa admin bilan bog'laning!** 💬
