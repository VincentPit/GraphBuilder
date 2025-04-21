import logging
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from urllib.parse import urljoin, urlparse

def get_documents_from_web_page(source_url:str):
  try:
    pages = WebBaseLoader(source_url).load()
    file_name = pages[0].metadata['title']
    return file_name, pages
  except Exception as e:
    job_status = "Failed"
    message="Failed To Process Web URL"
    error_message = str(e)
    logging.error(f"Failed To Process Web URL: {file_name}")
    logging.exception(f'Exception Stack trace: {error_message}')
    return 

def get_documents_from_web_pageX(source_url: str, max_depth: int = 2) -> dict:
    visited_urls = set()
    url_to_documents = {}

    def extract_links(url):
        """Extract all absolute HTTP(S) links from <a> tags on a page"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            links = set()

            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                full_url = urljoin(url, href)
                if full_url.startswith("http"):
                    links.add(full_url)

            return links
        except Exception as e:
            logging.warning(f"Failed to extract links from {url}: {e}")
            return set()

    def crawl(url, depth):
        if url in visited_urls or depth > max_depth:
            return

        visited_urls.add(url)

        try:
            pages = WebBaseLoader(url).load()
            title = pages[0].metadata.get("title", url)
            url_to_documents[title] = pages
            logging.info(f"[depth={depth}] Loaded '{title}' from {url}")
        except Exception as e:
            logging.warning(f"Failed to load {url}: {e}")
            return

        for link in extract_links(url):
            crawl(link, depth + 1)

    crawl(source_url, depth=0)
    return url_to_documents
