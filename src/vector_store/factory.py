from enum import Enum
from typing import Optional

from .base import BaseVectorStoreManager, VectorStoreConfig
from .in_memory import InMemoryVectorStoreManager
from .qdrant import QdrantVectorStoreManager

class VectorStoreType(Enum):
    """Enum for vector store types."""
    IN_MEMORY = "in_memory"
    QDRANT = "qdrant"

class VectorStoreFactory:
    """Factory for creating vector store managers."""
    
    @staticmethod
    def create_vector_store_manager(
        embeddings,
        store_type: VectorStoreType = VectorStoreType.IN_MEMORY,
        config: Optional[VectorStoreConfig] = None
    ) -> BaseVectorStoreManager:
        """
        Create a vector store manager.
        
        Args:
            embeddings: Embedding model.
            store_type (VectorStoreType): Type of vector store.
            config (Optional[VectorStoreConfig]): Configuration for vector store.
        
        Returns:
            BaseVectorStoreManager: Configured vector store manager.
        """
        managers = {
            VectorStoreType.IN_MEMORY: InMemoryVectorStoreManager,
            VectorStoreType.QDRANT: QdrantVectorStoreManager
        }
        
        manager_class = managers.get(store_type)
        if not manager_class:
            raise ValueError(f"Unsupported vector store type: {store_type}")
        
        return manager_class(embeddings, config)

# Convenience function
def create_vector_store(
    embeddings, 
    use_in_memory_store: bool = True,
    config: Optional[VectorStoreConfig] = None
):
    """
    Convenience function to create a vector store.
    
    Args:
        embeddings: Embedding model.
        use_in_memory_store (bool): Flag to use in-memory or Qdrant store.
        config (Optional[VectorStoreConfig]): Configuration for vector store.
    
    Returns:
        Vector store instance.
    """
    store_type = (
        VectorStoreType.IN_MEMORY 
        if use_in_memory_store 
        else VectorStoreType.QDRANT
    )
    
    manager = VectorStoreFactory.create_vector_store_manager(
        embeddings, 
        store_type, 
        config
    )
    
    return manager.create_vector_store()