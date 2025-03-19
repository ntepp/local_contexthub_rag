import os
import urllib.parse
from typing import List, Optional
from langchain_core.documents import Document

def is_url(source: str) -> bool:
    """
    Check if the source is a URL.
    
    Args:
        source (str): Source to check
    
    Returns:
        bool: True if source is a URL, False otherwise
    """
    try:
        result = urllib.parse.urlparse(source)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def is_local_file(source: str) -> bool:
    """
    Check if the source is a local file.
    
    Args:
        source (str): Source to check
    
    Returns:
        bool: True if source is a local file, False otherwise
    """
    # Normalize path for both Linux and Windows
    normalized_path = os.path.normpath(source)
    
    # Check if file exists and is a file
    return os.path.isfile(normalized_path)

def determine_source_type(source: str) -> str:
    """
    Determine the type of source.
    
    Args:
        source (str): Source to analyze
    
    Returns:
        str: Source type ('url', 'pdf', 'unknown')
    """
    if is_url(source):
        return 'url'
    
    if is_local_file(source):
        # Check file extension for PDFs
        if source.lower().endswith('.pdf'):
            return 'pdf'
    
    return 'unknown'