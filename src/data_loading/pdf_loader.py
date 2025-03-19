from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from abc import ABC, abstractmethod
from typing import List, Union
import os

from src.data_loading.abstract_loader import DataLoader


class PDFDataLoader(DataLoader):
    def __init__(self, file_path: str):
        """
        Initialize PDF loader.
        
        Args:
            file_path (str): Path to the PDF file
        """
        self.file_path = file_path
        
        # Validate file exists and is a PDF
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"Not a PDF file: {file_path}")
        
        # Create the Langchain PDF loader
        self._loader = PyPDFLoader(self.file_path)
    
    def load(self) -> List[Document]:
        """
        Load PDF using Langchain's PyPDFLoader.
        
        Returns:
            List[Document]: PDF content as documents
        """
        try:
            # Use the pre-created loader to load documents
            return self._loader.load()
        
        except Exception as e:
            raise RuntimeError(f"Error loading PDF {self.file_path}: {str(e)}")

# Convenience function
def load_pdf(file_path: str) -> List[Document]:
    """
    Load PDF file and return as Langchain Documents.
    
    Args:
        file_path (str): Path to the PDF file
    
    Returns:
        List[Document]: PDF content as documents
    """
    loader = PDFDataLoader(file_path)
    return loader.load()

# Multiple PDF loader
class MultiplePDFLoader(DataLoader):
    def __init__(self, directory_path: str):
        """
        Initialize loader for multiple PDFs in a directory.
        
        Args:
            directory_path (str): Path to directory containing PDFs
        """
        self.directory_path = directory_path
        
        # Validate directory exists
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")
    
    def load(self) -> List[Document]:
        """
        Load all PDFs from a directory.
        
        Returns:
            List[Document]: Combined documents from all PDFs
        """
        all_documents = []
        
        # Iterate through PDF files in the directory
        for filename in os.listdir(self.directory_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(self.directory_path, filename)
                
                try:
                    # Load documents from each PDF
                    pdf_documents = PDFDataLoader(file_path).load()
                    all_documents.extend(pdf_documents)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return all_documents

# Convenience function for multiple PDFs
def load_pdfs_from_directory(directory_path: str) -> List[Document]:
    """
    Load all PDFs from a directory.
    
    Args:
        directory_path (str): Path to directory containing PDFs
    
    Returns:
        List[Document]: Combined documents from all PDFs
    """
    loader = MultiplePDFLoader(directory_path)
    return loader.load()