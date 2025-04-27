from .ML.embedding import CustomVietnameseEmbedding
from .model_setup import load_model_Llama3
from .Agent.agent import Agent
from typing import List

class ChatbotBase:
    def __init__(self):
        self.llm = load_model_Llama3()
        self.embedding = CustomVietnameseEmbedding()
        self.agent = Agent(self.llm, self.embedding)

    def process_documents(self, file_paths: List[str], original_names: List[str]):
        return self.agent.process_documents(file_paths, original_names)
        
    def initialize_agent(self):
        """Initialize the agent with Llama3 model"""
        return self.agent.setup_agent_executor()
        
    def generate_agent_response(self, user_input: str, chat_history: list = None, session_id="default_user") -> str:
        """Generate response using the Llama3 agent"""
        return self.agent.run_agent(user_input, chat_history)
