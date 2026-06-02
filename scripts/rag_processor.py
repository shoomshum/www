"""ระบบ RAG สำหรับค้นหาเอกสารและสร้างสรุป"""
import os
import requests
from build_knowledge_base import TeachingKnowledgeBase

class RAGProcessor:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = 'https://api.deepseek.com/v1/chat/completions'
        self.kb = TeachingKnowledgeBase()
    
    def search_docs(self, query):
        return self.kb.search(query)
    
    def generate_summary(self, lecture_text):
        """สร้างสรุปบทเรียนพร้อม RAG"""
        # ค้นหาเอกสารที่เกี่ยวข้อง
        results = self.search_docs(lecture_text)
        
        # สร้าง context
        context = ""
        if results['documents']:
            for i, doc in enumerate(results['documents'][0][:5]):
                filename = results['metadatas'][0][i]['filename']
                context += f"\n### จาก {filename}:\n{doc[:500]}\n"
        
        # Prompt สำหรับ DeepSeek
        prompt = f"""คุณเป็นผู้ช่วยสร้างสรุปบทเรียนฟิสิกส์

เนื้อหาบรรยาย:
{lecture_text}

เอกสารประกอบที่เกี่ยวข้อง:
{context}

สร้างสรุปเป็น Markdown:
1. หัวข้อบทเรียน
2. จุดประสงค์การเรียนรู้ (3-5 ข้อ)
3. เนื้อหาสรุป (ใช้ LaTeX $$...$$ สำหรับสมการ)
4. แบบฝึกหัดและเฉลย (อ้างอิงเอกสารประกอบ)
5. คำสำคัญ (tags)"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.5,
            'max_tokens': 4000
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
