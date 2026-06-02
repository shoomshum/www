# check_environment.py
import sys
print('Python version:', sys.version)

try:
    import whisper
    print('✅ Whisper installed')
except:
    print('❌ Whisper not installed')

try:
    import chromadb
    print('✅ ChromaDB installed')
except:
    print('❌ ChromaDB not installed')

try:
    from sentence_transformers import SentenceTransformer
    print('✅ Sentence Transformers installed')
except:
    print('❌ Sentence Transformers not installed')

try:
    import torch
    print('✅ PyTorch installed')
except:
    print('❌ PyTorch not installed')

try:
    import requests
    print('✅ Requests installed')
except:
    print('❌ Requests not installed')
