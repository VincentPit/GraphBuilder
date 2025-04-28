from processing import extract_graph_from_file_local_file, create_source_node_graph_dfrobot_url, extract_graph_from_web_page
from shared.common_fn import create_graph_database_connection
import os
from dbAccess import graphDBdataAccess
import logging
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

visited = set()
queue = Queue()
processed_urls = set() 

def extract_links(url):
    """Extract all links from the page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return [urljoin(url, a.get('href')) for a in soup.find_all('a') if a.get('href')]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []

def process_url(graph, model, allowed_nodes, allowed_relationship, url):
    """Crawl and process a single URL."""
    if url in visited or url in processed_urls:
        return

    if 'dfrobot' not in url:
        logging.info(f"Skipping URL without keyword: {url}")
        return

    visited.add(url)
    logging.info(f"Processing: {url}")

    # First, process the source node graph for this URL
    lst_file, success_count, fail_count = create_source_node_graph_dfrobot_url(graph, model, url, "dfrobot")
    logging.info(f"Processed source node for {url}: Success: {success_count}, Failures: {fail_count}")

    # Then, extract the graph from the page
    result_dic = extract_graph_from_web_page(graph, model, url, allowed_nodes, allowed_relationship)
    logging.info(f"Extracted graph data from {url}: {result_dic}")

    # Extract and queue the new links for crawling
    links = extract_links(url)
    for link in links:
        queue.put(link)  # Add the new link to the queue

def crawl_urls_in_parallel(graph, model, allowed_nodes, allowed_relationship, delay=1, max_workers=5):
    """Crawl URLs in parallel and process them."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while not queue.empty():
            url = queue.get()
            executor.submit(process_url, graph, model, allowed_nodes, allowed_relationship, url)
            time.sleep(delay)  # Be nice to the server
            
def main(start_urls, graph, model, allowed_nodes, allowed_relationship):
    # Enqueue all the starting URLs
    for url in start_urls:
        queue.put(url)

    # Start crawling and processing URLs in parallel
    crawl_urls_in_parallel(graph, model, allowed_nodes, allowed_relationship)

if __name__ == "__main__":
    
    #To Be Modified
    uri = "bolt://localhost:7687"
    userName = "neo4j"
    password = "369369St"
    database = "neo4j"
    model = "azure_ai_gpt_4o"
    allowedNodes = "controller,sensor,board,actor,module,software"
    allowedRelationships = "兼容"
    
    graph = create_graph_database_connection(uri, userName, password, database)   
    graphDb_data_Access = graphDBdataAccess(graph)

    
    """这是我们的网站：
    https://www.dfrobot.com.cn/
    论坛和创客社区：
    https://makelog.dfrobot.com.cn/
    https://mc.dfrobot.com.cn/
    商城：
    https://www.dfrobot.com.cn/index.php
    wiki:
    https://wiki.dfrobot.com.cn/"""
    
    start_urls = ["https://www.dfrobot.com.cn/", 
                  "https://makelog.dfrobot.com.cn/", 
                  "https://mc.dfrobot.com.cn/", 
                  "https://www.dfrobot.com.cn/index.php", 
                  "https://wiki.dfrobot.com.cn/"] 

    CHUNK_DIR = os.path.join(os.path.dirname(__file__), "chunks")
    MERGED_DIR = os.path.join(os.path.dirname(__file__), "data")

    logging.info(f"Starting crawl with initial URLs: {start_urls}")
    
    main(start_urls, graph, model, allowedNodes, allowedRelationships)
