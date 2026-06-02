"""แปลงไฟล์เสียง MP3 เป็นข้อความด้วย Whisper"""
import whisper
import os
from pathlib import Path
from datetime import datetime, timedelta
from pydub import AudioSegment

class ThaiTranscriber:
    def __init__(self, model_size="medium"):
        print(f"🔄 โหลดโมเดล Whisper ({model_size})...")
        self.model = whisper.load_model(model_size)
        print("✅ พร้อม")
    
    def transcribe(self, audio_path, language="th"):
        print(f"🎤 ถอดความ: {audio_path}")
        
        # แปลงเป็น wav ถ้าจำเป็น
        if not audio_path.endswith('.wav'):
            audio = AudioSegment.from_file(audio_path)
            audio = audio.set_channels(1).set_frame_rate(16000)
            wav_path = str(Path(audio_path).with_suffix('.wav'))
            audio.export(wav_path, format="wav")
        else:
            wav_path = audio_path
        
        # ถอดความ
        result = self.model.transcribe(
            wav_path,
            language=language,
            verbose=True,
            initial_prompt="บทเรียนฟิสิกส์ วิชาฟิสิกส์"
        )
        
        return result
    
    def save_transcript(self, result, output_path, with_timestamps=True):
        """บันทึกข้อความ"""
        text = ""
        for seg in result["segments"]:
            if with_timestamps:
                start = str(timedelta(seconds=int(seg["start"])))
                end = str(timedelta(seconds=int(seg["end"])))
                text += f"[{start} - {end}] {seg['text'].strip()}\n\n"
            else:
                text += seg['text'].strip() + "\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return output_path

def process_audio_files(audio_dir="audio_recordings", output_dir="_raw_lectures"):
    """ประมวลผลไฟล์เสียงทั้งหมด"""
    audio_dir = Path(audio_dir)
    output_dir = Path(output_dir)
    processed_dir = audio_dir / "processed"
    
    output_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)
    
    # หาไฟล์เสียงใหม่
    audio_files = []
    for ext in ['*.mp3', '*.wav', '*.m4a']:
        audio_files.extend(audio_dir.glob(ext))
    
    if not audio_files:
        print("📭 ไม่พบไฟล์เสียง")
        return []
    
    transcriber = ThaiTranscriber(model_size="medium")
    processed = []
    
    for audio_file in audio_files:
        print(f"\n📁 {audio_file.name}")
        
        # ถอดความ
        result = transcriber.transcribe(str(audio_file))
        
        # สร้างชื่อไฟล์จากวันที่
        date_match = audio_file.stem[:10] if len(audio_file.stem) >= 10 else None
        date_str = date_match if date_match else datetime.now().strftime('%Y-%m-%d')
        output_name = f"{date_str}-lecture.txt"
        output_path = output_dir / output_name
        
        # บันทึกแบบไม่มี timestamp (สำหรับใช้กับ RAG)
        transcriber.save_transcript(result, str(output_path), with_timestamps=False)
        
        # ย้ายไฟล์เสียง
        audio_file.rename(processed_dir / audio_file.name)
        
        print(f"✅ {output_path}")
        processed.append(str(output_path))
    
    return processed

if __name__ == "__main__":
    process_audio_files()