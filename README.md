# GraphBuilder

The project was built for DFRobot Co.. The objectives were to build a knowledge graph based on the company's webpages, so as to work with the RAG system. 
The project was based on prior works of ![llm-graph-builder](https://github.com/BinNong/llm-graph-builder.git)
Chinese version of README.md is here https://github.com/VincentPit/GraphBuilder/blob/main/README_ZH.md. 
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Potential](#potential)

## Installation

Instructions on how to install or set up the project.

```bash
git clone https://github.com/VincentPit/GraphBuilder.git
```
The project is using Conda for environment management, so make sure conda is available at your terminal.

To initiate the conda environment, run 

```bash 
conda env create -f environment.yml
conda activate graph
pip install -r condaenv.rnehk3uw.requirements.txt
```

Now, make sure GPU using CUDA api and Neo4j database 5.21 is available on your device. 

Here is how to install Neo4j 5.21 with apoc extension along. 
```bash 
sudo apt-get install cypher-shell=1:5.21.0
sudo apt-get install neo4j=1:5.21.0

neo4j --version
cypher-shell --version
sudo apt-get update
```
Now, you have Neo4j database. You would need apoc for the project to run. 

```bash 
sudo find / -name "neo4j.conf"
```

Find the file, use ```bash vi neo4j.conf``` or ```bash nano neo4j.conf``` to modify the file to allow apoc extension. 

Big chances that the file is in /etc/neo4j/

Put these in the corresponding lines. 

```bash 
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,apoc.*
```
Find the plugins directory of your local neo4j. 

Download APOC from ![apoc](https://github.com/neo4j/apoc/releases/download/5.21.0/apoc-5.21.0-core.jar) and place the file in plugins. 

The last step needed to set up would be environment variable assignments:

```bash 
export UPDATE_GRAPH_CHUNKS_PROCESSED=20
export EMBEDDING_MODEL=all-MiniLM-L6-v2
export IS_EMBEDDING=TRUE
export LLM_MODEL_CONFIG_azure_ai_gpt_4o= your_model,url,key,version
export NUMBER_OF_CHUNKS_TO_COMBINE=6
``` 

Try and run 
```bash 
python main_test.py
``` 
to see if any error pops up. Solve them before proceed.

## Usage

If you have local Json files and want to build Knowledge Graph with them. If you wish to do so by batch, use sample_fromJson.py to specify and get what items in the Json file intended.
Then, by specifying file name of Json, run 
```bash 
python main_json.py
``` 
to start building graph. 

If you wish to fetch urls to process, use 
```bash 
python main_url_sync.py
``` 
or 
```bash 
python main_url.py
``` 
for multi-processing. 

If you wish to fetch all links before proceeding to graph building, use 
```bash 
python sync_urlRetriever.py
``` 
first to fetch urls and run 
```bash 
python main_para.py
``` 
to process the urls in parallel. 

##Potential

I am also trying to embed the pictures of the components. The visual embeddings could be placed as attributes to the component nodes.
Since we are searching with text embeddings, so far there is only one type fo model that is available, that fits the task, CLIP. 
If we are to use to CLIP, we need to embed all text with the same text processing model that has been used by the CLIP model we choose. 
We need to switch the embedding model to CLIP's text model, and embed images with CLIP's visual model.