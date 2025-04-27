class ResponseGenerator:
    def __init__(self, agent):
        self.agent = agent
        
    def generate_agent_response(self, message, chat_history: list = None):
        """Generate response using the Llama3 agent"""
        return self.agent.run_agent(message, chat_history)