import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from langchain_core.prompts import PromptTemplate
from typing_extensions import List, TypedDict
from langchain_core.prompts import PromptTemplate
from src.data_loading.text_splitter import split_text
from src.data_loading.loaders import load_data_from_web
from src.vector_store.embeddings import initialize_embeddings
from src.vector_store.store import create_vector_store
from src.llm.llm_chain import initialize_model_llm
from src.utils.cache import cache_url, get_redis_client, is_url_cached


embeddings = initialize_embeddings()
vector_store = create_vector_store(embeddings, use_in_memory_store=False)

# 1. Load and chunk contents of the blog

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible. 
If you don't know the answer, explain why you don't know.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
prompt = PromptTemplate.from_template(template)


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    llm = initialize_model_llm()
    response = llm.invoke(messages)
    return {"answer": response.content}

def load_source(post_url):
    client = get_redis_client()
    if not is_url_cached(client, post_url):
        docs = load_data_from_web(url=post_url)
        # 2. Split Data
        all_splits = split_text(docs)
        # Index chunks
        _ = vector_store.add_documents(documents=all_splits)
        cache_url(client, post_url)
        print(f"URL '{post_url}' cached successfully.")
def create_and_run_graph(question):
    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    response = graph.invoke({"question": question})
    return response["answer"]
    