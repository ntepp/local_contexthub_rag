from typing import List
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain.docstore.document import Document

from .base import BaseVectorStoreManager, VectorStoreConfig

class QdrantVectorStoreManager(BaseVectorStoreManager):
    """Manager for Qdrant vector store."""
    
    def __init__(
        self, 
        embeddings, 
        config: VectorStoreConfig = None
    ):
        """
        Initialize Qdrant vector store manager.
        
        Args:
            embeddings: Embedding model.
            config (VectorStoreConfig, optional): Configuration for vector store.
        """
        super().__init__(embeddings)
        self._config = config or VectorStoreConfig()
        self._client = QdrantClient(url=self._config.url or "http://localhost:6333")
    
    def create_vector_store(self) -> QdrantVectorStore:
        """
        Create a Qdrant vector store.
        
        Returns:
            QdrantVectorStore: Configured Qdrant vector store.
        """
        print("Using Qdrant for vector storage")
        
        # Check and create collection if not exists
        try:
            self._client.get_collection(collection_name=self._config.collection_name)
            print(f"Collection '{self._config.collection_name}' already exists.")
        except Exception:
            print(f"Collection '{self._config.collection_name}' does not exist, creating it.")
            self._client.create_collection(
                collection_name=self._config.collection_name,
                vectors_config={
                    "size": self._config.vector_size, 
                    "distance": self._config.distance_metric
                }
            )
        
        return QdrantVectorStore(
            client=self._client, 
            collection_name=self._config.collection_name, 
            embedding=self._embeddings
        )
    
    def document_exists(self, identifier: str) -> bool:
        """
        Check if a document exists in the Qdrant vector store.
        
        Args:
            identifier (str): URL or unique identifier.
        
        Returns:
            bool: True if document exists, False otherwise.
        """
        vector_store = self.create_vector_store()
        results = vector_store.similarity_search(identifier, k=1)
        return len(results) > 0
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the Qdrant vector store.
        
        Args:
            documents (List[Document]): Documents to add.
        """
        vector_store = self.create_vector_store()
        vector_store.add_documents(documents)