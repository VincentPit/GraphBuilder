import os
import json
import logging
import time
from threading import Lock
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dbAccess import graphDBdataAccess
from processing import create_source_node_graph_dfrobot_url, extract_graph_from_web_page
from shared.common_fn import create_graph_database_connection

logging.basicConfig(level=logging.INFO)
#To Be Modified
uri = "bolt://localhost:7687"
userName = "neo4j"
password = "369369St"
database = "neo4j"
model = "azure_ai_gpt_4o"
allowedNodes = "controller,sensor,board,actor,module"
allowedRelationships = "兼容"

CHUNK_DIR = os.path.join(os.path.dirname(__file__), "chunks")
MERGED_DIR = os.path.join(os.path.dirname(__file__), "data")
#try
file_name = "/home/dfrobot/ljy/GraphBuilder/data/sample.json"


graph = create_graph_database_connection(uri, userName, password, database)   

graphDb_data_Access = graphDBdataAccess(graph)

merged_file_path = os.path.join(MERGED_DIR,file_name)
logging.info(f'File path:{merged_file_path}')
url = "https://wiki.dfrobot.com.cn/"
# First, process the source node graph for this URL
lst_file, success_count, fail_count = create_source_node_graph_dfrobot_url(graph, model, url, "dfrobot")
logging.info(f"Processed source node for {url}: Success: {success_count}, Failures: {fail_count}")

# Then, extract the graph from the page
result_dic = extract_graph_from_web_page(graph, model, url, allowedNodes, allowedRelationships)
logging.info(f"Extracted graph data from {url}: {result_dic}")
