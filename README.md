# GraphBuilder

The project was built for DFRobot Co.. The objectives were to build a knowledge graph based on the company's webpages, so as to work with the RAG system. 
The project was based on prior works of ![llm-graph-builder](https://github.com/BinNong/llm-graph-builder.git)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)


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

Try and run ```bash python main_test.py``` to see if any error pops up. Solve them before proceed.

##Usage

If you have local Json files and want to build Knowlege Graph with them. If you wish to do so by batch, use sample_fromJson.py to specify and get what items in the Json file intended.
Then, by specifying file name of Json, run ```bash python main_json.py``` to start building graph. 

If you wish to fetch urls to process, use ```bash python main_url_sync.py``` or ```bash python main_url.py``` for multi-processing. 

If you wish to fetch all links before proceeding to graph building, use ```bash python sync_urlRetriever.py``` first to fetch urls and run ```bash python main_para.py``` to process the urls in parallel. 