from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..RAG.file_loader import PDFLoader
from ..RAG.setup_spilitter import TextSplitter
from ..RAG.vectorstore import VectorDB
from ..RAG.setup_retriever import Retriever
from typing import List

class Agent():
    def __init__(self, llm, embedding):
        self.llm = llm
        self.embedding = embedding
        self.pdf_loader = None
        self.splitter_class = TextSplitter()
        self.vectorstore_class = None
        self.vectorstore = None
        self.retriever_class = Retriever()
        self.retriever = None
        self.agent_executor = None

    def process_documents(self, file_paths: List[str], original_names: List[str]):
        self.pdf_loader = PDFLoader(file_paths, original_names)
        documents = self.pdf_loader.load_docs()
        docs = self.splitter_class.splitter_documents(documents)
        self.vectorstore_class = VectorDB(docs=docs, 
                                    embedding=self.embedding,
                                    )
        self.vectorstore = self.vectorstore_class.get_vectorstore()
        self.retriever = self.retriever_class.build_retriever(docs, 4)
        return "Documents processed successfully"

    def get_ensemble_retriever(self):
        ensemble_retriever = self.retriever_class.get_ensemble_retriever(vectorstore=self.vectorstore, retriever=self.retriever)
        return ensemble_retriever
    
    def setup_agent_executor(self):
        """Set up the LLama3 agent with retrieval tools"""
        if not self.vectorstore or not self.retriever:
            raise ValueError("You need to process documents first by calling process_documents")
            
        # Create a retrieval tool
        retriever = self.get_ensemble_retriever()
        retriever_tool = create_retriever_tool(
            retriever=retriever,
            name="tìm_kiếm_tài_liệu",
            description="Tìm kiếm và truy xuất thông tin từ các tài liệu đã tải lên. Sử dụng công cụ này khi bạn cần trả lời các câu hỏi về thông tin cụ thể trong tài liệu."
        )
        
        tools = [retriever_tool]
        system_prompt = """Bạn là một trợ lý AI chuyên trả lời các câu hỏi dựa vào tài liệu được cung cấp. 
                        Chỉ dựa vào thông tin tìm được từ công cụ và kiến thức nội tại của bạn về chủ đề này để trả lời. 
                        Nếu không tìm thấy thông tin trong tài liệu, hãy nói rằng bạn không có thông tin đó trong tài liệu được cung cấp. 
                        Luôn trả lời bằng tiếng Việt một cách rõ ràng và chi tiết nhất có thể dựa trên thông tin có được."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            handle_parsing_errors=True,
        )
        
        return self.agent_executor
    
    def run_agent(self, user_input: str, chat_history: list = None):
        if self.agent_executor is None:
            self.setup_agent_executor()
        return self.agent_executor.invoke({"input": user_input, "chat_history": chat_history})
