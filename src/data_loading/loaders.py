import bs4
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader
import os

def load_data_from_web(url: str):
    loader = WebBaseLoader(url, bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header","article")
        )   ))
    data = loader.load()
    return data


def preview_data(data, num_docs=2, num_chars=200):
    """Previews the loaded data."""
    for i, doc in enumerate(data[:num_docs]):
        print(f"Document {i}:")
        print(doc.page_content[:num_chars] + "...")
