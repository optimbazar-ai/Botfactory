"""
Bilimlar Bazasi - Bot uchun maxsus ma'lumotlar
"""
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class KnowledgeBase:
    """Bot uchun bilimlar bazasi"""
    
    def __init__(self, bot_id: int, db=None):
        """
        Bilimlar bazasini ishga tushirish
        
        Args:
            bot_id: Bot ID
            db: Database obyekti
        """
        self.bot_id = bot_id
        self.db = db
        self.knowledge_file = f"knowledge/bot_{bot_id}.json"
        
        # Bilimlar bazasi strukturasi
        self.knowledge = {
            "faq": [],           # Tez-tez so'raladigan savollar
            "facts": [],         # Faktlar va ma'lumotlar
            "instructions": [],  # Ko'rsatmalar va qoidalar
            "contacts": [],      # Kontaktlar
            "products": [],      # Mahsulotlar/xizmatlar
            "custom": []         # Maxsus ma'lumotlar
        }
        
        # Bilimlarni yuklash
        self.load_knowledge()
        
        # TF-IDF vektorizator (o'xshash savollarni topish uchun)
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2)
        )
        self.vectors = None
        self.update_vectors()
    
    def load_knowledge(self):
        """Bilimlar bazasini fayldan yuklash"""
        try:
            os.makedirs("knowledge", exist_ok=True)
            
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
        except Exception as e:
            print(f"❌ Bilimlarni yuklashda xatolik: {e}")
    
    def save_knowledge(self):
        """Bilimlar bazasini faylga saqlash"""
        try:
            os.makedirs("knowledge", exist_ok=True)
            
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
                
            # Vektorlarni yangilash
            self.update_vectors()
            
            return True
        except Exception as e:
            print(f"❌ Bilimlarni saqlashda xatolik: {e}")
            return False
    
    def add_faq(self, question: str, answer: str, keywords: List[str] = None):
        """Tez-tez so'raladigan savol qo'shish"""
        faq_item = {
            "id": len(self.knowledge["faq"]) + 1,
            "question": question,
            "answer": answer,
            "keywords": keywords or [],
            "usage_count": 0,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["faq"].append(faq_item)
        self.save_knowledge()
        
        return faq_item
    
    def add_fact(self, title: str, content: str, category: str = "general"):
        """Fakt yoki ma'lumot qo'shish"""
        fact_item = {
            "id": len(self.knowledge["facts"]) + 1,
            "title": title,
            "content": content,
            "category": category,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["facts"].append(fact_item)
        self.save_knowledge()
        
        return fact_item
    
    def add_instruction(self, title: str, steps: List[str]):
        """Ko'rsatma qo'shish"""
        instruction_item = {
            "id": len(self.knowledge["instructions"]) + 1,
            "title": title,
            "steps": steps,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["instructions"].append(instruction_item)
        self.save_knowledge()
        
        return instruction_item
    
    def add_contact(self, name: str, phone: str = None, telegram: str = None, email: str = None):
        """Kontakt qo'shish"""
        contact_item = {
            "id": len(self.knowledge["contacts"]) + 1,
            "name": name,
            "phone": phone,
            "telegram": telegram,
            "email": email,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["contacts"].append(contact_item)
        self.save_knowledge()
        
        return contact_item
    
    def add_product(self, name: str, description: str, price: str = None, image_url: str = None):
        """Mahsulot/xizmat qo'shish"""
        product_item = {
            "id": len(self.knowledge["products"]) + 1,
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["products"].append(product_item)
        self.save_knowledge()
        
        return product_item
    
    def find_answer(self, question: str) -> Optional[str]:
        """Savolga javob topish"""
        
        # 1. To'g'ridan-to'g'ri moslik qidirish
        for faq in self.knowledge["faq"]:
            if self.is_similar_text(question.lower(), faq["question"].lower(), threshold=0.8):
                # Foydalanish sonini oshirish
                faq["usage_count"] += 1
                self.save_knowledge()
                return faq["answer"]
        
        # 2. Kalit so'zlar bo'yicha qidirish
        question_words = set(question.lower().split())
        
        for faq in self.knowledge["faq"]:
            if faq["keywords"]:
                keywords = set([k.lower() for k in faq["keywords"]])
                if len(question_words.intersection(keywords)) > 0:
                    faq["usage_count"] += 1
                    self.save_knowledge()
                    return faq["answer"]
        
        # 3. TF-IDF orqali o'xshash savollarni topish
        similar_answer = self.find_similar_faq(question)
        if similar_answer:
            return similar_answer
        
        # 4. Faktlar va ma'lumotlardan qidirish
        relevant_facts = self.search_facts(question)
        if relevant_facts:
            return self.format_facts_response(relevant_facts)
        
        # 5. Mahsulotlardan qidirish
        relevant_products = self.search_products(question)
        if relevant_products:
            return self.format_products_response(relevant_products)
        
        return None
    
    def is_similar_text(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Ikki matn o'xshashligini tekshirish"""
        # Oddiy Jaccard similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        
        return similarity >= threshold
    
    def update_vectors(self):
        """TF-IDF vektorlarini yangilash"""
        try:
            all_texts = []
            
            # FAQ savollarini yig'ish
            for faq in self.knowledge["faq"]:
                all_texts.append(faq["question"])
            
            if all_texts:
                self.vectors = self.vectorizer.fit_transform(all_texts)
        except Exception as e:
            print(f"❌ Vektorlarni yangilashda xatolik: {e}")
    
    def find_similar_faq(self, question: str, threshold: float = 0.5) -> Optional[str]:
        """TF-IDF yordamida o'xshash FAQ topish"""
        try:
            if self.vectors is None or self.vectors.shape[0] == 0:
                return None
            
            # Savol vektorini hisoblash
            question_vector = self.vectorizer.transform([question])
            
            # Cosine similarity hisoblash
            similarities = cosine_similarity(question_vector, self.vectors).flatten()
            
            # Eng o'xshash FAQ ni topish
            max_similarity_idx = np.argmax(similarities)
            max_similarity = similarities[max_similarity_idx]
            
            if max_similarity >= threshold:
                faq = self.knowledge["faq"][max_similarity_idx]
                faq["usage_count"] += 1
                self.save_knowledge()
                return faq["answer"]
            
        except Exception as e:
            print(f"❌ O'xshash FAQ topishda xatolik: {e}")
        
        return None
    
    def search_facts(self, query: str) -> List[Dict]:
        """Faktlardan qidirish"""
        relevant = []
        query_words = set(query.lower().split())
        
        for fact in self.knowledge["facts"]:
            title_words = set(fact["title"].lower().split())
            content_words = set(fact["content"].lower().split())
            
            if query_words.intersection(title_words) or query_words.intersection(content_words):
                relevant.append(fact)
        
        return relevant[:3]  # Maksimum 3 ta fakt
    
    def search_products(self, query: str) -> List[Dict]:
        """Mahsulotlardan qidirish"""
        relevant = []
        query_words = set(query.lower().split())
        
        for product in self.knowledge["products"]:
            name_words = set(product["name"].lower().split())
            desc_words = set(product["description"].lower().split())
            
            if query_words.intersection(name_words) or query_words.intersection(desc_words):
                relevant.append(product)
        
        return relevant[:3]  # Maksimum 3 ta mahsulot
    
    def format_facts_response(self, facts: List[Dict]) -> str:
        """Faktlarni javob formatiga keltirish"""
        response = "📚 Topilgan ma'lumotlar:\n\n"
        
        for fact in facts:
            response += f"**{fact['title']}**\n"
            response += f"{fact['content']}\n\n"
        
        return response.strip()
    
    def format_products_response(self, products: List[Dict]) -> str:
        """Mahsulotlarni javob formatiga keltirish"""
        response = "🛍️ Topilgan mahsulotlar:\n\n"
        
        for product in products:
            response += f"**{product['name']}**\n"
            response += f"{product['description']}\n"
            if product["price"]:
                response += f"💰 Narxi: {product['price']}\n"
            response += "\n"
        
        return response.strip()
    
    def get_statistics(self) -> Dict:
        """Bilimlar bazasi statistikasi"""
        stats = {
            "total_faq": len(self.knowledge["faq"]),
            "total_facts": len(self.knowledge["facts"]),
            "total_instructions": len(self.knowledge["instructions"]),
            "total_contacts": len(self.knowledge["contacts"]),
            "total_products": len(self.knowledge["products"]),
            "most_used_faq": None
        }
        
        # Eng ko'p ishlatilgan FAQ
        if self.knowledge["faq"]:
            most_used = max(self.knowledge["faq"], key=lambda x: x.get("usage_count", 0))
            if most_used["usage_count"] > 0:
                stats["most_used_faq"] = {
                    "question": most_used["question"],
                    "usage_count": most_used["usage_count"]
                }
        
        return stats
    
    def export_to_prompt(self) -> str:
        """Bilimlar bazasini AI prompt formatiga eksport qilish"""
        prompt = "BOT BILIMLARI:\n\n"
        
        # FAQ
        if self.knowledge["faq"]:
            prompt += "TEZ-TEZ SO'RALADIGAN SAVOLLAR:\n"
            for faq in self.knowledge["faq"][:10]:  # Maksimum 10 ta
                prompt += f"S: {faq['question']}\n"
                prompt += f"J: {faq['answer']}\n\n"
        
        # Faktlar
        if self.knowledge["facts"]:
            prompt += "\nASSOSIY MA'LUMOTLAR:\n"
            for fact in self.knowledge["facts"][:5]:
                prompt += f"- {fact['title']}: {fact['content']}\n"
        
        # Kontaktlar
        if self.knowledge["contacts"]:
            prompt += "\nKONTAKTLAR:\n"
            for contact in self.knowledge["contacts"]:
                prompt += f"- {contact['name']}"
                if contact["phone"]:
                    prompt += f" Tel: {contact['phone']}"
                if contact["telegram"]:
                    prompt += f" Telegram: {contact['telegram']}"
                prompt += "\n"
        
        return prompt
    
    def add_document(self, filename: str, content: str, description: str = ""):
        """
        Fayldan yuklangan hujjatni bilim bazasiga qo'shish
        
        Args:
            filename: Fayl nomi
            content: Fayl matni
            description: Fayl tavsifi
        """
        document = {
            "id": self._generate_id("custom"),
            "filename": filename,
            "content": content,
            "description": description,
            "upload_date": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        self.knowledge["custom"].append(document)
        self.save_knowledge()
        self.update_vectors()
        
        print(f"✅ Hujjat qo'shildi: {filename}")
    
    def delete_document(self, doc_id: int):
        """
        Hujjatni o'chirish
        
        Args:
            doc_id: Hujjat ID
        """
        self.knowledge["custom"] = [
            doc for doc in self.knowledge["custom"]
            if doc.get("id") != doc_id
        ]
        self.save_knowledge()
        self.update_vectors()
        
        print(f"✅ Hujjat o'chirildi: ID {doc_id}")
    
    def get_documents(self) -> List[Dict]:
        """Barcha yuklangan hujjatlarni olish"""
        return self.knowledge.get("custom", [])


if __name__ == "__main__":
    # Test uchun bilimlar bazasi yaratish
    kb = KnowledgeBase(bot_id=1)
    
    # FAQ qo'shish
    kb.add_faq(
        "Sizning ish vaqtingiz qanday?",
        "Biz 24/7 online rejimda ishlaymiz. Istalgan vaqt murojaat qilishingiz mumkin!",
        ["ish vaqti", "qachon", "soat"]
    )
    
    kb.add_faq(
        "Qanday xizmatlar ko'rsatasiz?",
        "Biz Telegram bot yaratish, sozlash va boshqarish xizmatlarini ko'rsatamiz.",
        ["xizmat", "nima", "qanday"]
    )
    
    # Fakt qo'shish
    kb.add_fact(
        "BotFactory haqida",
        "BotFactory - bu kod yozmasdan Telegram bot yaratish platformasi.",
        "general"
    )
    
    # Kontakt qo'shish
    kb.add_contact(
        "Admin",
        phone="+998996448444",
        telegram="@Akramjon1984"
    )
    
    # Mahsulot qo'shish
    kb.add_product(
        "Premium Obuna",
        "Cheksiz bot yaratish va boshqarish imkoniyati",
        "145,000 so'm/oy"
    )
    
    # Test qidiruv
    print("🔍 Test qidiruv:")
    
    test_questions = [
        "Qachon ishlaysiz?",
        "Nima xizmat ko'rsatasiz?",
        "Admin kontakti",
        "Premium narxi qancha?"
    ]
    
    for q in test_questions:
        answer = kb.find_answer(q)
        print(f"\nS: {q}")
        print(f"J: {answer or 'Javob topilmadi'}")
    
    # Statistika
    print("\n📊 Statistika:")
    stats = kb.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
