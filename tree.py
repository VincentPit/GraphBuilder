import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

class TreeNode:
    def __init__(self, url):
        self.url = url
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"TreeNode(url={self.url})"
    
    def to_dict(self):
        """Convert the tree structure into a dictionary."""
        return {
            'url': self.url,
            'children': [child.to_dict() for child in self.children]
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a tree from a dictionary."""
        node = cls(data['url'])
        for child_data in data['children']:
            node.add_child(cls.from_dict(child_data))
        return node