from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set
import logging
from abc import ABC, abstractmethod

from src.data_loading.abstract_loader import DataLoader


class WebsiteDataLoader(DataLoader):
    def __init__(
        self, 
        base_url: str, 
        max_pages: int = 100, 
        depth: int = 1,
        allowed_domains: List[str] = None
    ):
        """
        Initialize website crawler.
        
        Args:
            base_url (str): Starting URL to crawl
            max_pages (int): Maximum number of pages to crawl
            depth (int): Maximum crawl depth
            allowed_domains (List[str]): Domains to restrict crawling
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.depth = depth
        self.allowed_domains = allowed_domains or [urlparse(base_url).netloc]
        
        # Tracking sets
        self.visited_urls: Set[str] = set()
        self.urls_to_crawl: Set[str] = {base_url}
        
        # Crawler results
        self.crawled_content: List[dict] = []
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid for crawling.
        
        Args:
            url (str): URL to validate
        
        Returns:
            bool: Whether URL is valid
        """
        parsed_url = urlparse(url)
        
        # Check domain restrictions
        domain_valid = any(
            allowed_domain in parsed_url.netloc 
            for allowed_domain in self.allowed_domains
        )
        
        # Exclude non-http(s) and already visited URLs
        return (
            parsed_url.scheme in ['http', 'https'] and
            domain_valid and
            url not in self.visited_urls
        )
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract links from HTML content.
        
        Args:
            html (str): HTML content
            base_url (str): Base URL for resolving relative links
        
        Returns:
            List[str]: Extracted links
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if self._is_valid_url(link):
                links.append(link)
        
        return links
    
    def load(self) -> List[Document]:
        """
        Crawl the entire website.
        
        Returns:
            List[Document]: Crawled page contents
        """
        current_depth = 0
        
        while self.urls_to_crawl and len(self.crawled_content) < self.max_pages:
            # Break if max depth reached
            if current_depth > self.depth:
                break
            
            # Get next URL to crawl
            current_url = self.urls_to_crawl.pop()
            
            try:
                # Fetch page content
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                
                # Mark as visited
                self.visited_urls.add(current_url)
                
                # Create Langchain Document
                document = Document(
                    page_content=response.text,
                    metadata={
                        'source': current_url
                    }
                )
                
                # Store document
                self.crawled_content.append(document)
                
                # Extract new links
                new_links = self._extract_links(response.text, current_url)
                
                # Add new links to crawl queue
                self.urls_to_crawl.update(
                    link for link in new_links 
                    if link not in self.visited_urls
                )
            
            except requests.RequestException as e:
                logging.error(f"Error crawling {current_url}: {e}")
            
            current_depth += 1
        
        return self.crawled_content

# Convenience function
def load_entire_website(
    url: str, 
    max_pages: int = 100, 
    depth: int = 1,
    allowed_domains: List[str] = None
) -> List[Document]:
    """
    Load entire website content.
    
    Args:
        url (str): Starting URL to crawl
        max_pages (int): Maximum number of pages to crawl
        depth (int): Maximum crawl depth
        allowed_domains (List[str]): Domains to restrict crawling
    
    Returns:
        List[Document]: Crawled page contents
    """
    crawler = WebsiteDataLoader(
        base_url=url, 
        max_pages=max_pages, 
        depth=depth,
        allowed_domains=allowed_domains
    )
    return crawler.load()
