import bs4
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader
import os

def load_data_from_web(url: str):
    loader = WebBaseLoader(url, bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )   ))
    data = loader.load()
    return data

def load_data_from_local(local_path: str):
    """Loads documents from a local directory or file."""
    if os.path.isdir(local_path):
        loader = DirectoryLoader(
            local_path,
            glob="**/*",  # Load all files recursively
            loader_cls=get_loader_class,
        )
    elif os.path.isfile(local_path):
        loader = get_loader_class(local_path)(local_path)
    else:
        raise ValueError(f"Invalid path: {local_path}")
    data = loader.load()
    return data

def get_loader_class(file_path: str):
    """Returns the appropriate loader class based on the file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return TextLoader
    elif ext == ".pdf":
        return PyPDFLoader
    elif ext == ".docx":
        return Docx2txtLoader
    else:
        return TextLoader #Default to text loader
def preview_data(data, num_docs=2, num_chars=200):
    """Previews the loaded data."""
    for i, doc in enumerate(data[:num_docs]):
        print(f"Document {i}:")
        print(doc.page_content[:num_chars] + "...")
