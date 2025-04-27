from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from typing import List
class PDFLoader():
    def __init__(self, paths: List[str], original_names: List[str]):
        self.pdf_paths = paths
        self.original_names = original_names
    def load_docs(self) -> List[Document]:
        documents = []
        for i, path in enumerate(self.pdf_paths):
            loader = PyPDFLoader(path)
            pages = loader.load() 
            combined_content = "\n".join([page.page_content for page in pages])
            doc = Document(
                page_content=combined_content, 
                metadata={"source": path, "doc_name": self.original_names[i]} 
            )
            documents.append(doc)
        return documents