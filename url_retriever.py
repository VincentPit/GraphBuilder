import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from tree import TreeNode
import random

# Function to extract links from a webpage
def get_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            full_links = [urljoin(url, link['href']) for link in links]
            return full_links
        else:
            print(f"Failed to retrieve page: {url}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []

# Recursive function to build the tree structure
def build_tree(url, visited, parent_node=None):
    if url in visited:
        return
    visited.add(url)  # Mark the URL as visited
    print(f"Building Tree from {url} ...")
    # Add the current URL as a child of the parent node
    current_node = TreeNode(url)
    if parent_node is not None:
        parent_node.add_child(current_node)

    # Extract path segments
    path_segments = urlparse(url).path.strip('/').split('/')

    # Get links from the current page
    links = get_links(url)

    for link in links:
        # Build the next URL's path, based on the current URL
        next_url = urljoin(url, link)

        # Ensure the link follows the same segment structure
        next_segments = urlparse(next_url).path.strip('/').split('/')
        if next_segments[:len(path_segments)] == path_segments:
            build_tree(next_url, visited, current_node)
        time.sleep(random.uniform(0.5, 2))

# Function to start crawling and build tree from a root URL
def crawl(start_url, max_depth=5):
    print(f"Crawling from {start_url} ...")
    visited = set()  # Set to store visited URLs
    root_node = TreeNode(start_url)  # The root node of the tree
    build_tree(start_url, visited, root_node)
    return root_node

# Function to save the tree structure to a JSON file
def save_tree_to_file(tree, filename):
    with open(filename, 'w') as f:
        json.dump(tree.to_dict(), f, indent=4)

# Function to load the tree structure from a JSON file
def load_tree_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return TreeNode.from_dict(data)

def print_tree(node, level=0):
    print('  ' * level + f"URL: {node.url}")
    for child in node.children:
        print_tree(child, level + 1)

if __name__ == "__main__":
    start_url = 'https://wiki.dfrobot.com.cn/'
    root_tree = crawl(start_url, max_depth=4)
    save_tree_to_file(root_tree, 'tree_structure.json')

    loaded_tree = load_tree_from_file('tree_structure.json')



    print("Loaded Tree:")
    print_tree(loaded_tree)