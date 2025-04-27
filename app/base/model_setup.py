from langchain_community.chat_models import ChatOllama
from transformers import AutoTokenizer, AutoModel
import os
ENCODER_MODEL_NAME = 'bkai-foundation-models/vietnamese-bi-encoder'
MODEL_LLMs_NAME = 'Llama-3.2-1B-Instruct-Q4_0.gguf'
MAX_TOKENS = 2048

def load_vietnamese_encoder_model():
    model_name = ENCODER_MODEL_NAME
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

def load_model_Llama3():
    llm = ChatOllama(model="llama3", temperature=0.1 ,max_tokens=MAX_TOKENS) 
    return llm