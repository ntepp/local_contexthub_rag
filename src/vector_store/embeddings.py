from langchain_ollama.embeddings import OllamaEmbeddings


def initialize_embeddings():
    """Initializes OpenAI embeddings."""
    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    return embeddings
