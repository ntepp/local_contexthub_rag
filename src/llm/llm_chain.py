from langchain_ollama import ChatOllama


def initialize_model_llm(model_name="deepseek-r1"):

    llm = ChatOllama(
    model=model_name,
    temperature=0,
    # other params...
    )
    return llm