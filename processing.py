import json
import logging
import os
from datetime import datetime
import hashlib
from dbAccess import graphDBdataAccess
from typing import List
from src.entities.source_node import sourceNode
from langchain_text_splitters import TokenTextSplitter
from langchain.docstore.document import Document
from langchain_community.graphs import Neo4jGraph
from llm import generate_graphDocuments
from shared.common_fn import load_embedding_model, save_graphDocuments_in_neo4j,get_chunk_and_graphDocument,delete_uploaded_local_file
import shutil
from local_file import get_documents_from_file_by_path

logging.basicConfig(format="%(asctime)s - %(message)s", level="INFO")
class CreateChunksofDocument:
    def __init__(self, pages: list[Document], graph: Neo4jGraph):
        self.pages = pages
        self.graph = graph

    def split_file_into_chunks(self):
        """
        Split a list of documents(file pages) into chunks of fixed size.

        Args:
            pages: A list of pages to split. Each page is a list of text strings.

        Returns:
            A list of chunks each of which is a langchain Document.
        """
        logging.info("Split file into smaller chunks")
        # number_of_chunks_allowed = int(os.environ.get('NUMBER_OF_CHUNKS_ALLOWED'))
        text_splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=20)
        if 'page' in self.pages[0].metadata:
            chunks = []
            for i, document in enumerate(self.pages):
                page_number = i + 1
                for chunk in text_splitter.split_documents([document]):
                    chunks.append(Document(page_content=chunk.page_content, metadata={'page_number':page_number}))    
        else:
            chunks = text_splitter.split_documents(self.pages)
        return chunks
    
def create_relation_between_chunks(graph, file_name, chunks: List[Document])->list:
    logging.info("creating FIRST_CHUNK and NEXT_CHUNK relationships between chunks")
    current_chunk_id = ""
    lst_chunks_including_hash = []
    batch_data = []
    relationships = []
    offset=0
    for i, chunk in enumerate(chunks):
        page_content_sha1 = hashlib.sha1(chunk.page_content.encode())
        previous_chunk_id = current_chunk_id
        current_chunk_id = page_content_sha1.hexdigest()
        position = i + 1 
        if i>0:
            #offset += len(tiktoken.encoding_for_model("gpt2").encode(chunk.page_content))
            offset += len(chunks[i-1].page_content)
        if i == 0:
            firstChunk = True
        else:
            firstChunk = False  
        metadata = {"position": position,"length": len(chunk.page_content), "content_offset":offset}
        chunk_document = Document(
            page_content=chunk.page_content, metadata=metadata
        )
        
        chunk_data = {
            "id": current_chunk_id,
            "pg_content": chunk_document.page_content,
            "position": position,
            "length": chunk_document.metadata["length"],
            "f_name": file_name,
            "previous_id" : previous_chunk_id,
            "content_offset" : offset
        }
        
        if 'page_number' in chunk.metadata:
            chunk_data['page_number'] = chunk.metadata['page_number']
         
        if 'start_time' in chunk.metadata and 'end_time' in chunk.metadata:
            chunk_data['start_time'] = chunk.metadata['start_time']
            chunk_data['end_time'] = chunk.metadata['end_time'] 
               
        batch_data.append(chunk_data)
        
        lst_chunks_including_hash.append({'chunk_id': current_chunk_id, 'chunk_doc': chunk})
        
        # create relationships between chunks
        if firstChunk:
            relationships.append({"type": "FIRST_CHUNK", "chunk_id": current_chunk_id})
        else:
            relationships.append({
                "type": "NEXT_CHUNK",
                "previous_chunk_id": previous_chunk_id,  # ID of previous chunk
                "current_chunk_id": current_chunk_id
            })
          
    query_to_create_chunk_and_PART_OF_relation = """
        UNWIND $batch_data AS data
        MERGE (c:Chunk {id: data.id})
        SET c.text = data.pg_content, c.position = data.position, c.length = data.length, c.fileName=data.f_name, c.content_offset=data.content_offset
        WITH data, c
        SET c.page_number = CASE WHEN data.page_number IS NOT NULL THEN data.page_number END,
            c.start_time = CASE WHEN data.start_time IS NOT NULL THEN data.start_time END,
            c.end_time = CASE WHEN data.end_time IS NOT NULL THEN data.end_time END
        WITH data, c
        MATCH (d:Document {fileName: data.f_name})
        MERGE (c)-[:PART_OF]->(d)
    """
    graph.query(query_to_create_chunk_and_PART_OF_relation, params={"batch_data": batch_data})
    
    query_to_create_FIRST_relation = """ 
        UNWIND $relationships AS relationship
        MATCH (d:Document {fileName: $f_name})
        MATCH (c:Chunk {id: relationship.chunk_id})
        FOREACH(r IN CASE WHEN relationship.type = 'FIRST_CHUNK' THEN [1] ELSE [] END |
                MERGE (d)-[:FIRST_CHUNK]->(c))
        """
    graph.query(query_to_create_FIRST_relation, params={"f_name": file_name, "relationships": relationships})   
    
    query_to_create_NEXT_CHUNK_relation = """ 
        UNWIND $relationships AS relationship
        MATCH (c:Chunk {id: relationship.current_chunk_id})
        WITH c, relationship
        MATCH (pc:Chunk {id: relationship.previous_chunk_id})
        FOREACH(r IN CASE WHEN relationship.type = 'NEXT_CHUNK' THEN [1] ELSE [] END |
                MERGE (c)<-[:NEXT_CHUNK]-(pc))
        """
    graph.query(query_to_create_NEXT_CHUNK_relation, params={"relationships": relationships})   
    
    return lst_chunks_including_hash

def update_embedding_create_vector_index(graph, chunkId_chunkDoc_list, file_name):
    #create embedding
    isEmbedding = os.getenv('IS_EMBEDDING')
    embedding_model = os.getenv('EMBEDDING_MODEL')
    
    embeddings, dimension = load_embedding_model(embedding_model)
    logging.info(f'embedding model:{embeddings} and dimesion:{dimension}')
    data_for_query = []
    logging.info(f"update embedding and vector index for chunks")
    for row in chunkId_chunkDoc_list:
        # for graph_document in row['graph_doc']:
        if isEmbedding.upper() == "TRUE":
            embeddings_arr = embeddings.embed_query(row['chunk_doc'].page_content)
            # logging.info(f'Embedding list {embeddings_arr}')
                                    
            data_for_query.append({
                "chunkId": row['chunk_id'],
                "embeddings": embeddings_arr
            })
            # graph.query("""MATCH (d:Document {fileName : $fileName})
            #                MERGE (c:Chunk {id:$chunkId}) SET c.embedding = $embeddings 
            #                MERGE (c)-[:PART_OF]->(d)
            #             """,
            #             {
            #                 "fileName" : file_name,
            #                 "chunkId": row['chunk_id'],
            #                 "embeddings" : embeddings_arr
            #             }
            #             )
            # logging.info('create vector index on chunk embedding')

            graph.query("""CREATE VECTOR INDEX `vector` if not exists for (c:Chunk) on (c.embedding)
                            OPTIONS {indexConfig: {
                            `vector.dimensions`: $dimensions,
                            `vector.similarity_function`: 'cosine'
                            }}
                        """,
                        {
                            "dimensions" : dimension
                        }
                        )
    
    query_to_create_embedding = """
        UNWIND $data AS row
        MATCH (d:Document {fileName: $fileName})
        MERGE (c:Chunk {id: row.chunkId})
        SET c.embedding = row.embeddings
        MERGE (c)-[:PART_OF]->(d)
    """       
    graph.query(query_to_create_embedding, params={"fileName":file_name, "data":data_for_query})

def merge_relationship_between_chunk_and_entites(graph: Neo4jGraph, graph_documents_chunk_chunk_Id : list):
    batch_data = []
    logging.info("Create HAS_ENTITY relationship between chunks and entities")
    chunk_node_id_set = 'id:"{}"'
    for graph_doc_chunk_id in graph_documents_chunk_chunk_Id:
        for node in graph_doc_chunk_id['graph_doc'].nodes:
            query_data={
                'chunk_id': graph_doc_chunk_id['chunk_id'],
                'node_type': node.type,
                'node_id': node.id
            }
            batch_data.append(query_data)
            #node_id = node.id
            #Below query is also unable to change as parametrize because we can't make parameter of Label or node type
            #https://neo4j.com/docs/cypher-manual/current/syntax/parameters/
            #graph.query('MATCH(c:Chunk {'+chunk_node_id_set.format(graph_doc_chunk_id['chunk_id'])+'}) MERGE (n:'+ node.type +'{ id: "'+node_id+'"}) MERGE (c)-[:HAS_ENTITY]->(n)')
          
    if batch_data:
        unwind_query = """
                    UNWIND $batch_data AS data
                    MATCH (c:Chunk {id: data.chunk_id})
                    CALL apoc.merge.node([data.node_type], {id: data.node_id}) YIELD node AS n
                    MERGE (c)-[:HAS_ENTITY]->(n)
                """
        graph.query(unwind_query, params={"batch_data": batch_data})
        
def processing_chunks(chunkId_chunkDoc_list,graph,file_name,model,allowedNodes,allowedRelationship, node_count, rel_count):
  #create vector index and update chunk node with embedding
  update_embedding_create_vector_index( graph, chunkId_chunkDoc_list, file_name)
  logging.info("Get graph document list from models")
  graph_documents =  generate_graphDocuments(model, graph, chunkId_chunkDoc_list, allowedNodes, allowedRelationship)
  save_graphDocuments_in_neo4j(graph, graph_documents)
  chunks_and_graphDocuments_list = get_chunk_and_graphDocument(graph_documents, chunkId_chunkDoc_list)
  merge_relationship_between_chunk_and_entites(graph, chunks_and_graphDocuments_list)
  # return graph_documents
  
  distinct_nodes = set()
  relations = []
  for graph_document in graph_documents:
    #get distinct nodes
    for node in graph_document.nodes:
          node_id = node.id
          node_type= node.type
          if (node_id, node_type) not in distinct_nodes:
            distinct_nodes.add((node_id, node_type))
  #get all relations
  for relation in graph_document.relationships:
        relations.append(relation.type)

  node_count += len(distinct_nodes)
  rel_count += len(relations)
  print(f'node count internal func:{node_count}')
  print(f'relation count internal func:{rel_count}')
  return node_count,rel_count

def processing_source(graph, model, file_name, text_data, allowedNodes, allowedRelationship, is_uploaded_from_local=None, merged_file_path=None):
    """
    Extracts a Neo4jGraph from a JSON text input based on the model.
    
    Args:
        graph: The graph object to interact with the graph database.
        model: Type of model to use ('Diffbot' or 'OpenAI GPT').
        file_name: The name of the file.
        text_data: List of text entries from the JSON file.
        allowedNodes: Allowed nodes for the graph.
        allowedRelationship: Allowed relationships for the graph.
        is_uploaded_from_local: If the file was uploaded locally.
        merged_file_path: The path to the uploaded file (if local). 
    
    Returns:
        A dictionary with fileName, nodeCount, relationshipCount, processingTime, status, and model.
    """
    start_time = datetime.now()
    graphDb_data_Access = graphDBdataAccess(graph)

    result = graphDb_data_Access.get_current_status_document_node(file_name)
    logging.info("Processing text data into chunks")

    # Clean and split text data into chunks
    bad_chars = ['"', "\n", "'"]
    cleaned_text_data = []
    for text in text_data:
        for char in bad_chars:
            text = text.replace(char, ' ')
        cleaned_text_data.append(text)

    create_chunks_obj = CreateChunksofDocument(cleaned_text_data, graph)
    chunks = create_chunks_obj.split_file_into_chunks()
    chunkId_chunkDoc_list = create_relation_between_chunks(graph, file_name, chunks)

    if result[0]['Status'] != 'Processing':
        obj_source_node = sourceNode()
        status = "Processing"
        obj_source_node.file_name = file_name
        obj_source_node.status = status
        obj_source_node.total_chunks = len(chunks)
        obj_source_node.total_text_entries = len(cleaned_text_data)
        obj_source_node.model = model
        graphDb_data_Access.update_source_node(obj_source_node)
        
        logging.info(f"Updated status for {file_name} to 'Processing'")

        # Process in batches of chunks
        update_graph_chunk_processed = int(os.environ.get('UPDATE_GRAPH_CHUNKS_PROCESSED'))
        is_cancelled_status = False
        job_status = "Completed"
        node_count = 0
        rel_count = 0

        for i in range(0, len(chunkId_chunkDoc_list), update_graph_chunk_processed):
            select_chunks_upto = i + update_graph_chunk_processed
            if len(chunkId_chunkDoc_list) <= select_chunks_upto:
                select_chunks_upto = len(chunkId_chunkDoc_list)
            selected_chunks = chunkId_chunkDoc_list[i:select_chunks_upto]

            result = graphDb_data_Access.get_current_status_document_node(file_name)
            is_cancelled_status = result[0]['is_cancelled']
            if bool(is_cancelled_status) is True:
                job_status = "Cancelled"
                logging.info('Exit from processing due to cancellation')
                exit

            node_count, rel_count = processing_chunks(selected_chunks, graph, file_name, model, allowedNodes, allowedRelationship, node_count, rel_count)

            end_time = datetime.now()
            processed_time = end_time - start_time

            # Update source node after each batch
            obj_source_node = sourceNode()
            obj_source_node.file_name = file_name
            obj_source_node.updated_at = end_time
            obj_source_node.processing_time = processed_time
            obj_source_node.node_count = node_count
            obj_source_node.processed_chunk = select_chunks_upto
            obj_source_node.relationship_count = rel_count
            graphDb_data_Access.update_source_node(obj_source_node)

        result = graphDb_data_Access.get_current_status_document_node(file_name)
        is_cancelled_status = result[0]['is_cancelled']
        if bool(is_cancelled_status) is True:
            logging.info(f'Cancelled at the end of extraction')
            job_status = 'Cancelled'

        logging.info(f'Final Job Status: {job_status}')
        end_time = datetime.now()
        processed_time = end_time - start_time

        obj_source_node = sourceNode()
        obj_source_node.file_name = file_name
        obj_source_node.status = job_status
        obj_source_node.processing_time = processed_time

        graphDb_data_Access.update_source_node(obj_source_node)
        logging.info(f'Updated nodeCount and relCount for {file_name}')

        # Cleanup local file if necessary
        if is_uploaded_from_local:
            delete_uploaded_local_file(merged_file_path, file_name)

        return {
            "fileName": file_name,
            "nodeCount": node_count,
            "relationshipCount": rel_count,
            "processingTime": round(processed_time.total_seconds(), 2),
            "status": job_status,
            "model": model,
            "success_count": 1
        }
    else:
        logging.info(f'File {file_name} is already in "Processing" status.')

def extract_graph_from_file_local_file(graph, model, merged_file_path, fileName, allowedNodes, allowedRelationship,uri):

    logging.info(f'Process file name :{fileName}')
    file_name, pages, file_extension = get_documents_from_file_by_path(merged_file_path,fileName)
    if pages==None or len(pages)==0:
        raise Exception(f'File content is not available for file : {file_name}')

    return processing_source(graph, model, file_name, pages, allowedNodes, allowedRelationship, True, merged_file_path, uri)

def merge_chunks_local(file_name, total_chunks, chunk_dir, merged_dir):
    if not os.path.exists(merged_dir):
        os.mkdir(merged_dir)
    logging.info(f'Merged File Path: {merged_dir}')
    merged_file_path = os.path.join(merged_dir, file_name)
    with open(merged_file_path, "wb") as write_stream:
        for i in range(1,total_chunks+1):
            chunk_file_path = os.path.join(chunk_dir, f"{file_name}_part_{i}")
            logging.info(f'Chunk File Path While Merging Parts:{chunk_file_path}')
            with open(chunk_file_path, "rb") as chunk_file:
                shutil.copyfileobj(chunk_file, write_stream)
            os.unlink(chunk_file_path)  # Delete the individual chunk file after merging
    logging.info("Chunks merged successfully and return file size")
    file_name, pages, _ = get_documents_from_file_by_path(merged_file_path,file_name)
    pdf_total_pages = pages[0].metadata['total_pages']
    file_size = os.path.getsize(merged_file_path)
    return pdf_total_pages,file_size