from typing import Annotated, Dict
from processing import extract_graph_from_file_local_file
from shared.common_fn import create_graph_database_connection
import uvicorn
import asyncio
import base64
import json
import os
from dbAccess import graphDBdataAccess
from datetime import datetime, timezone
import time
import logging

#To Be Modified
uri = "bolt://localhost:7687"
userName = "root"
password = "dfrobot"
database = "neo4j"
model = "azure"
allowedNodes = ""
allowedRelationship = ""

CHUNK_DIR = os.path.join(os.path.dirname(__file__), "chunks")
MERGED_DIR = os.path.join(os.path.dirname(__file__), "data")

file_name = "products_wiki_zh.json"


graph = create_graph_database_connection(uri, userName, password, database)   

graphDb_data_Access = graphDBdataAccess(graph)

merged_file_path = os.path.join(MERGED_DIR,file_name)
logging.info(f'File path:{merged_file_path}')

result = extract_graph_from_file_local_file(graph, model, merged_file_path, file_name, allowedNodes, allowedRelationship, uri)
