from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama

load_dotenv()

def initialize_model_llm(model_name=None):
    # Try env variable if model_name not passed
    model_name = model_name or os.getenv("LLM_MODEL_NAME")

    # Raise error if no model name provided
    if not model_name:
        raise ValueError(
            "No model name provided for LLM initialization.\n"
            "Please set the environment variable 'LLM_MODEL_NAME' in .env"
            "or pass a model name directly to initialize_model_llm(model_name='your_model')."
        )
    llm = ChatOllama(
    model=model_name,
    temperature=0,
    # other params...
    )
    return llm