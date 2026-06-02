"""สร้างไฟล์ Jekyll post จากสรุปบทเรียน"""
import os
import re
import yaml
from datetime import datetime
from rag_processor import RAGProcessor

def create_post(lecture_text, date_str=None):
    processor = RAGProcessor()
    
    # สร้างสรุปด้วย RAG
    print("🧠 กำลังสร้างสรุปด้วย DeepSeek + RAG...")
    summary = processor.generate_summary(lecture_text)
    
    # ดึงหัวข้อ
    title_match = re.search(r'# (.+)', summary)
    title = title_match.group(1) if title_match else "บทเรียน"
    
    # ดึง tags
    tags = ['ฟิสิกส์', 'lecture']
    tags_match = re.search(r'คำสำคัญ.*?:(.+?)(?:\n|$)', summary, re.IGNORECASE)
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(',')]
    
    # วันที่
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # สร้าง filename
    slug = title.lower().replace(' ', '-')[:50]
    filename = f"{date_obj.strftime('%Y-%m-%d')}-{slug}.md"
    filepath = os.path.join('_posts', filename)
    
    # Front matter
    front_matter = {
        'layout': 'post',
        'title': title,
        'date': date_obj.strftime('%Y-%m-%d %H:%M:%S +0700'),
        'categories': ['lectures'],
        'tags': tags,
        'comments': True,
        'math': True
    }
    
    # เขียนไฟล์
    os.makedirs('_posts', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(front_matter, f, allow_unicode=True)
        f.write('---\n\n')
        f.write(summary)
    
    print(f"✅ สร้างโพสต์: {filepath}")
    return filepath

def process_lecture_file(raw_file):
    """ประมวลผลไฟล์บรรยาย"""
    with open(raw_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ดึงวันที่จาก filename
    filename = os.path.basename(raw_file)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    date_str = date_match.group(1) if date_match else None
    
    return create_post(content, date_str)
