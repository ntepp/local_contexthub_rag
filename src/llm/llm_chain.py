import getpass
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()

def initialize_groq_llm():
    """Initializes the Groq LLM model."""
    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

    llm = init_chat_model("llama3-8b-8192", model_provider="groq")
    return llm