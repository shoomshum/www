#!/usr/bin/env python3
"""
Workflow อัตโนมัติ:
1. แปลงเสียง → ข้อความ (Whisper)
2. อัปเดต Knowledge Base (ChromaDB)
3. สร้างสรุป + โพสต์ (DeepSeek + RAG)
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def step1_speech_to_text():
    """ขั้นตอน 1: แปลงเสียงเป็นข้อความ"""
    print("\n" + "="*50)
    print("🔊 ขั้นตอน 1: ถอดความไฟล์เสียง")
    print("="*50)
    
    from speech_to_text import process_audio_files
    return process_audio_files()

def step2_update_knowledge_base():
    """ขั้นตอน 2: อัปเดตฐานความรู้"""
    print("\n" + "="*50)
    print("📚 ขั้นตอน 2: อัปเดต Knowledge Base")
    print("="*50)
    
    from build_knowledge_base import TeachingKnowledgeBase
    
    # เช็คว่ามีไฟล์ใหม่หรือไม่
    need_rebuild = False
    
    if not Path("vector_db").exists():
        need_rebuild = True
    else:
        last_build = Path("vector_db/last_build.txt")
        if last_build.exists():
            last_time = float(last_build.read_text())
            for root, dirs, files in os.walk("teaching_materials"):
                for f in files:
                    if os.path.getmtime(os.path.join(root, f)) > last_time:
                        need_rebuild = True
                        break
        else:
            need_rebuild = True
    
    if need_rebuild:
        kb = TeachingKnowledgeBase()
        kb.build()
        Path("vector_db/last_build.txt").write_text(str(datetime.now().timestamp()))
    else:
        print("✅ ไม่มีเอกสารใหม่")

def step3_generate_posts():
    """ขั้นตอน 3: สร้างโพสต์"""
    print("\n" + "="*50)
    print("📝 ขั้นตอน 3: สร้างสรุปและโพสต์")
    print("="*50)
    
    from generate_post import process_lecture_file
    
    raw_dir = Path("_raw_lectures")
    processed_dir = raw_dir / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    raw_files = list(raw_dir.glob("*.txt"))
    
    if not raw_files:
        print("📭 ไม่มีไฟล์บรรยาย")
        return
    
    for f in raw_files:
        print(f"\n📄 {f.name}")
        try:
            output = process_lecture_file(str(f))
            f.rename(processed_dir / f.name)
            print(f"✅ {output}")
        except Exception as e:
            print(f"❌ {e}")

def main():
    print("\n🚀 เริ่ม Daily Workflow")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    step1_speech_to_text()
    step2_update_knowledge_base()
    step3_generate_posts()
    
    print("\n" + "="*50)
    print("✅ เสร็จสมบูรณ์!")
    print("="*50)
    print("\nขั้นตอนต่อไป:")
    print("  1. ตรวจสอบ _posts/")
    print("  2. git add . && git commit -m 'update' && git push")
    print("\n🎉 GitHub Actions จะ deploy ให้อัตโนมัติ!")

if __name__ == "__main__":
    main()