from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

class TextSplitter():
    def __init__(self, 
                 separators: List[str] = ["\n\n", "\n", " ", ""],
                 chunk_size: int = 400,
                 chunk_overlap: int = 50
                 ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    def splitter_documents(self, documents: List[Document]):
        docs = self.splitter.split_documents(documents=documents)
        # for i, doc in enumerate(docs):
        #     print(f"--- Document {i+1} ---")
        #     print(doc.page_content)
        #     print(doc.metadata)
        #     print("\n")
        return docs
