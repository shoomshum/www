"""สร้างฐานความรู้จากเอกสารประกอบการสอน"""
import os
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import hashlib

class TeachingKnowledgeBase:
    def __init__(self):
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.client = chromadb.PersistentClient(path="vector_db")
        self.collection = self.client.get_or_create_collection(
            name="teaching_materials",
            embedding_function=self.embedding_fn
        )
    
    def extract_text(self, filepath):
        ext = Path(filepath).suffix.lower()
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def build(self):
        print("🔨 สร้าง Knowledge Base...")
        
        docs, metas, ids = [], [], []
        
        for root, dirs, files in os.walk("teaching_materials"):
            for file in files:
                if not file.endswith(('.txt', '.md')):
                    continue
                    
                filepath = os.path.join(root, file)
                text = self.extract_text(filepath)
                
                # แบ่งเป็น chunks
                chunk_size = 500
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    if not chunk.strip():
                        continue
                    
                    doc_id = hashlib.md5(f"{filepath}_{i}".encode()).hexdigest()
                    docs.append(chunk)
                    metas.append({"source": filepath, "filename": file})
                    ids.append(doc_id)
        
        if docs:
            self.collection.add(documents=docs, metadatas=metas, ids=ids)
            print(f"✅ เพิ่ม {len(docs)} ชิ้นจาก {len(set(m['filename'] for m in metas))} ไฟล์")
    
    def search(self, query, n=5):
        return self.collection.query(query_texts=[query], n_results=n)

if __name__ == "__main__":
    kb = TeachingKnowledgeBase()
    kb.build()
