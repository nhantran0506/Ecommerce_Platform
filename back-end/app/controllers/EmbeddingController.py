from bs4 import BeautifulSoup
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
import weaviate
from helper_collections.FAQQUES import FAQ
from typing import Optional, List
from models.Products import *
from config import (
    OLLAMA_CHAT_MODEL,
    OLLAMA_BASE_URL,
    WEAVIATE_URL,
    OLLAMA_EMBEDDING_MODEL
)
from models.CategoryProduct import CategoryProduct
from models.Category import Category
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db_connector import get_db
from serializers.ProductSerializers import ProductResponse

class EmbeddingController:
    def __init__(self, db: AsyncSession = Depends(get_db), collection_name: Optional[str] = "FAQ"):
        self.db = db
        self.client = weaviate.connect_to_local(
            host= WEAVIATE_URL,
        ) 
        
        self.embed_model = OllamaEmbedding(
            model_name=OLLAMA_EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
        
        
        self._create_schema(collection_name)
        
        self._vector_store = WeaviateVectorStore(
            weaviate_client=self.client,
            index_name=collection_name,
            text_key="content",
            metadata_keys=["topic"]
        )
        
        self._storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        
        self._index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            embed_model=self.embed_model,
        ).as_retriever()

    def _create_schema(self, collection_name):
        try:
            self.client.collections.get(self.collection_name)
        except:
            self.client.collections.create(
                name=collection_name,
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
            if collection_name == "FAQ":
                self.load_faq()


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

    async def embedding_product(self, product: Product):
        all_cat_names_query = select(CategoryProduct).where(CategoryProduct.product_id == product.product_id)
        results = await self.db.execute(all_cat_names_query)
        results = results.scalars()
        
        cat_names = ""
        for cat in results:
            cat_names_query = select(Category).where(Category.cat_id==cat.cat_id)
            cat = await self.db.execute(cat_names_query)
            cat_names += cat.scalar_one_or_none().cat_name

        product_text = f"{product.product_name * 3} {cat_names * 2}"
        product_doc = Document(
            text=product_text,
            metadata={"topic": "product", "product_id" : product.product_id}
        )

        self._index = VectorStoreIndex.from_documents(
            [product_doc],
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

        return bool(self._index)
    

    async def search_product(self, user_query : str):
        try:
            results = self._index.retrieve(user_query)
            product_ids = []
            for product in results or []:
                product_id = product.node.metadata.get('product_id', None)
                if product_id is None:
                    continue
                
                product_ids.append(product_id)
            
            product_get_query = select(Product).where(Product.product_id in product_ids)
            results = await self.db.execute(product_get_query)
            results =  [ProductResponse.model_validate(pro) for pro in results.scalars()]
        except Exception as e:
            await self.db.rollback()

        
            
    
    
    def embedding(self, docs: List[Document]):
        self._index = VectorStoreIndex.from_documents(
            docs,
            storage_context=self._storage_context,
            embed_model=self.embed_model,
        )

    def query(self, query: str, top_k: int = 5, min_similarity: float = 0.5):
        try:
            self.client.collections.get(self.collection_name)
        except weaviate.exceptions.WeaviateCollectionNotFoundException:
            self._create_schema()
        

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