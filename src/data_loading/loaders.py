import bs4
from langchain.document_loaders import WebBaseLoader

def load_data_from_web(url: str):
    loader = WebBaseLoader(url)
    data = loader.load()
    return data

def preview_data(data, num_docs=2, num_chars=200):
    """Previews the loaded data."""
    for i, doc in enumerate(data[:num_docs]):
        print(f"Document {i}:")
        print(doc.page_content[:num_chars] + "...")

if __name__ == "__main__":
    url = "https://lilianweng.github.io/posts/2023-06-23-anatomy-of-transformers-part-1/"
    loaded_data = load_data_from_web(url)
    preview_data(loaded_data)