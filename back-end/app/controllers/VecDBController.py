from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from typing import List

class VectorDBController():
    def __init__(self, db_path: str, db_name: str):
        self.rag_collection = None
        self.faq_collection = None

    def add_document(self, content : str):
        pass

    def add_documents(self, contents : List[str]):
        pass

    def search(self, query : str, from_db : str = "rag", top_k : int = 5):
        if from_db == "rag":
            return self.rag_collection.similarity_search(query, k=top_k)
        elif from_db == "faq":
            return self.faq_collection.similarity_search(query, k=top_k)
        else:
            return []

