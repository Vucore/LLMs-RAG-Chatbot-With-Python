from typing import Optional
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os
from ..services import services
import logging
from typing import List
router = APIRouter()
# Logging setup
logging.basicConfig(level=logging.INFO)

class FileNamesRequest(BaseModel):
    original_names: List[str]


class AgentRequest(BaseModel):
    message: str
    chat_history: list = None


@router.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{file.filename}"
    result = services.upload_file(filename, file.file)
    return {"status": "success", "file_path": result["file_path"], "original_name": result["original_name"]}

@router.post("/process_documents")
async def process_documents(request: FileNamesRequest):
    original_names = request.original_names
    result = services.process_documents(original_names)
    return {"status": "success", "message": result, "names": original_names}

@router.post("/run_agent")
async def run_agent(request: AgentRequest):
    user_input = request.message
    chat_history = request.chat_history
    return services.run_agent_rag(user_input, chat_history)