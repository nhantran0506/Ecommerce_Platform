from bs4 import BeautifulSoup
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import weaviate
from helper_collections.FAQQUES import FAQ
from typing import Optional, List
from models.Products import *

class EmbeddingController:
    def __init__(self, weaviate_url: str = "http://localhost:8080", collection_name: Optional[str] = "FAQ"):
        # Initialize Weaviate client
        self.client = weaviate.connect_to_local() 
        
        self.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url="http://localhost:11434",
        )
        
        self.collection_name = collection_name
        
        # Create schema if it doesn't exist
        self._create_schema()
        
        # Initialize vector store and index
        self._vector_store = WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=self.collection_name,
            text_key="content",
            metadata_keys=["topic"]
        )
        
        self._storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        
        self._index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            embed_model=self.embed_model,
        ).as_retriever()

    def _create_schema(self):
        """Create Weaviate schema for the collection if it doesn't exist"""
        class_obj = {
            "class": self.collection_name,
            "vectorizer": "none",  # we'll use our own embeddings
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                },
                {
                    "name": "topic",
                    "dataType": ["text"],
                }
            ]
        }
        
        # Check if class exists, if not create it
        try:
            self.client.collections.get(self.collection_name)
        except:
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config={"none": {"vectorizerModule": None}},
                properties=[
                    {
                        "name": "content",
                        "dataType": ["text"],
                    },
                    {
                        "name": "topic",
                        "dataType": ["text"],
                    }
                ]
            )

    def load_faq(self):
        docs = []
        for faq in FAQ:
            docs.append(Document(
                text=f"Question: {faq['question']} Answer: {faq['answer']}", 
                metadata={"topic": faq["topic"]}
            ))
        
        self._index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

    @staticmethod
    def embedding_html(html_content: str):
        doc = BeautifulSoup(html_content, "html.parser")
        return doc.get_text()

    def embedding_product(self, product: Product):
        product_text = f"{product.product_name} {product.product_description} {product.price}"
        return Document(
            text=product_text,
            metadata={"topic": "product"}
        )
    
    def embedding(self, docs: List[Document]):
        self._index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

    def query(self, query: str, top_k: int = 5, min_similarity: float = 0.6):
        results = self._index.retrieve(query)
        responses = []
        for node in results[:top_k] or []:
            if node.score >= min_similarity:
                responses.append({
                    'text': node.text,
                    'score': node.score
                })
        return responses

    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.client.collections.delete(self.collection_name)
            self._create_schema()
        except Exception as e:
            print(f"Error clearing collection: {e}")

    def __del__(self):
        """Destructor to properly close the Weaviate client connection"""
        if hasattr(self, 'client'):
            self.client.close()