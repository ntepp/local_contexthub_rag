import getpass
import os
from dotenv import load_dotenv

from langchain_ollama.embeddings import OllamaEmbeddings

load_dotenv()

def initialize_embeddings():
    """Initializes OpenAI embeddings."""
    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    return embeddings
