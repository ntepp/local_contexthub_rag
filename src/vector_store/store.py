from langchain_core.vectorstores import InMemoryVectorStore
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

# Function to check if a document exists
def document_exists(url: str, vector_store: QdrantVectorStore):
    # Query the collection using the URL as the unique identifier
    results = vector_store.similarity_search(url, k=1)
    print(results)
    return len(results) > 0

def create_vector_store(embeddings, use_in_memory_store=True):
    if use_in_memory_store:
        print("Using InMemoryVectorStore")
        vector_store = InMemoryVectorStore(embeddings)
        return vector_store
    else:
        collection_name = "post_collection"
        print("Using Qdrant for vector storage")
        qdrant_client = QdrantClient(url="http://localhost:6333")        
        
        try:
            qdrant_client.get_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' already exists.")
        except Exception as e:
            print(f"Collection '{collection_name}' does not exist, creating it.")
            qdrant_client.create_collection(collection_name=collection_name, vectors_config={"size": 768, "distance": "Cosine"})
            
        vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name, embedding=embeddings)

        return vector_store
