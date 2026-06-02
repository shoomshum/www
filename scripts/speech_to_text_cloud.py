"""
ใช้ DeepSeek API หรือ OpenAI API สำหรับถอดความ (เร็ว แต่มีค่าใช้จ่าย)
"""
import requests
import os
from pathlib import Path

def transcribe_with_deepseek(audio_path, api_key=None):
    """ใช้ DeepSeek API สำหรับถอดความ (ถ้ารองรับ)"""
    api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
    
    # DeepSeek อาจยังไม่รองรับ audio โดยตรง
    # วิธีนี้ยังไม่พร้อมใช้งาน รอ DeepSeek อัปเดต
    print("⚠️ DeepSeek ยังไม่รองรับ audio transcription โดยตรง")
    print("💡 แนะนำใช้ Whisper ในเครื่องแทน")
    return None

def transcribe_with_openai(audio_path, api_key=None):
    """ใช้ OpenAI Whisper API (ทางเลือก Cloud)"""
    import openai
    
    api_key = api_key or os.getenv('OPENAI_API_KEY')
    openai.api_key = api_key
    
    with open(audio_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="th",
            response_format="verbose_json"
        )
    
    return transcript