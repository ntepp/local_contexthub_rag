import getpass
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

load_dotenv()

def initialize_openai_embeddings():
    """Initializes OpenAI embeddings."""
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return embeddings
