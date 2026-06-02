"""ทดสอบแต่ละขั้นตอนแยกกัน"""
import sys
import os

def test_asr():
    """ทดสอบการถอดความ"""
    print("🧪 ทดสอบระบบถอดความ...")
    from speech_to_text import LectureAudioProcessor
    
    # ใช้โมเดลขนาดเล็กเพื่อทดสอบเร็ว
    processor = LectureAudioProcessor(model_size="base")
    
    # หาไฟล์เสียงไฟล์แรก
    audio_files = list(processor.audio_dir.glob("*.mp3"))
    if audio_files:
        print(f"ทดสอบกับไฟล์: {audio_files[0].name}")
        processor.process_lecture_audio(audio_files[0])
    else:
        print("❌ ไม่พบไฟล์เสียงสำหรับทดสอบ")

def test_rag():
    """ทดสอบการค้นหาเอกสาร"""
    print("🧪 ทดสอบระบบ RAG...")
    from rag_processor import RAGLectureProcessor
    
    processor = RAGLectureProcessor()
    query = "กฎการเคลื่อนที่ของนิวตัน"
    
    docs = processor.retrieve_relevant_docs(query)
    print(f"พบ {len(docs)} เอกสารที่เกี่ยวข้อง")
    
    for doc in docs[:3]:
        print(f"  - {doc['metadata']['filename']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "asr":
        test_asr()
    elif len(sys.argv) > 1 and sys.argv[1] == "rag":
        test_rag()
    else:
        print("วิธีใช้:")
        print("  python test_workflow.py asr  # ทดสอบระบบถอดความ")
        print("  python test_workflow.py rag  # ทดสอบระบบ RAG")