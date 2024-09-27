from bs4 import BeautifulSoup
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb
from helper_collections.FAQQUES import FAQ
from typing import Optional, List



class EmbeddingController:
    def __init__(self, db_path: Optional[str] = "./chroma_db", collection_name: Optional[str] = "faq"):
        self.db = chromadb.PersistentClient(path=db_path)
        self.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url="http://localhost:11434",
        )
        
        self.collection_name = collection_name
        self._chroma_collection = self.db.get_or_create_collection(collection_name)
        self._vector_store = ChromaVectorStore(chroma_collection=self._chroma_collection)
        self._storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        
        self._index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            embed_model=self.embed_model,
        ).as_retriever()

    def load_faq(self):
        docs = []
        for faq in FAQ:
            docs.append(Document(text=f"Question: {faq['question']} Answer: {faq['answer']}", metadata={"topic": faq["topic"]}))
        
        self._index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

    @staticmethod
    def embedding_html(html_content: str):
        doc = BeautifulSoup(html_content, "html.parser")
        return doc.get_text()

    def embedding(self, docs: List[Document]):
        self._index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

    def query(self, query: str, top_k: int = 5, min_similarity : float = 0.6):
        
        results = self._index.retrieve(
            query
        )
        responses = []
        for node in results[:top_k] or []:
            if node.score >= min_similarity:
                responses.append({
                    'text' : node.text,
                    'score' : node.score
                })
            
        return responses
        
