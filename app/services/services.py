from ..base.init import ChatbotBase
import os
from fastapi import UploadFile

chatbot = ChatbotBase()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded")

def upload_file(filename: str, file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        f.write(file.read())
    
    return {"file_path": file_path, "original_name": filename}

def process_documents(original_names: list):
    file_paths = [os.path.join(UPLOAD_DIR, name) for name in original_names]
    result = chatbot.process_documents(file_paths, original_names)
    return {"status": "success", "message": result, "names": original_names}

def run_agent_rag(user_input: str, chat_history: list = None):
    return chatbot.generate_agent_response(user_input, chat_history)