from src.data_loading.abstract_loader import DataLoader
import bs4
import os
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader

class WebDataLoader(DataLoader):
    def __init__(self, url: str):
        self.url = url
    
    def load(self):
        loader = WebBaseLoader(self.url)
        data = loader.load()
        return data
    