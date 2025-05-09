# 图谱构建器 (GraphBuilder)

该项目为DFRobot公司开发，目标是基于公司网站页面构建一个知识图谱，以便与RAG系统进行集成。
该项目基于之前的工作 [llm-graph-builder](https://github.com/BinNong/llm-graph-builder.git)。

## 目录

* [安装](#安装)
* [使用](#使用)
* [潜力](#潜力)

## 安装

### 安装步骤

首先克隆项目：

```bash
git clone https://github.com/VincentPit/GraphBuilder.git
```

该项目使用了Conda环境管理，请确保终端中已安装Conda。

为启动Conda环境，执行以下命令：

```bash
conda env create -f environment.yml
conda activate graph
pip install -r condaenv.rnehk3uw.requirements.txt
```

确保您的设备支持CUDA API和Neo4j数据库5.21。

### 安装Neo4j 5.21及APOC扩展

1. 安装Neo4j 5.21及cypher-shell：

```bash
sudo apt-get install cypher-shell=1:5.21.0
sudo apt-get install neo4j=1:5.21.0

neo4j --version
cypher-shell --version
sudo apt-get update
```

2. 安装完Neo4j后，您需要启用APOC扩展。在Neo4j配置文件中做如下修改：

```bash
sudo find / -name "neo4j.conf"
```

找到文件后，使用 `bash vi neo4j.conf` 或 `bash nano neo4j.conf` 打开并编辑。
可能的文件路径：`/etc/neo4j/`。

在文件中添加以下内容：

```bash
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,apoc.*
```

3. 找到Neo4j本地的插件目录，下载APOC插件并放入该目录：

下载地址：[APOC插件](https://github.com/neo4j/apoc/releases/download/5.21.0/apoc-5.21.0-core.jar)

4. 最后，设置以下环境变量：

```bash
export UPDATE_GRAPH_CHUNKS_PROCESSED=20
export EMBEDDING_MODEL=all-MiniLM-L6-v2
export IS_EMBEDDING=TRUE
export LLM_MODEL_CONFIG_azure_ai_gpt_4o=你的模型,url,key,version
export NUMBER_OF_CHUNKS_TO_COMBINE=6
```

5. 运行以下命令，检查是否有错误：

```bash
python main_test.py
```

如果有错误，解决后再继续。

## 使用

### 使用本地Json文件构建知识图谱

如果你有本地的Json文件并且想构建知识图谱，使用 `sample_fromJson.py` 来指定并获取Json文件中的目标项。
然后，指定文件名并运行以下命令来开始构建图谱：

```bash
python main_json.py
```

### 获取并处理网页URL

如果你需要抓取URL并处理它们，可以使用以下命令：

* 使用 `python main_url_sync.py` 抓取URL， 单线程处理。
* 使用 `python main_url.py` 进行多线程处理。

### 先抓取所有链接后再构建图谱

如果你想先抓取所有链接再进行图谱构建，先运行以下命令：

```bash
python sync_urlRetriever.py
```

然后，运行：

```bash
python main_para.py
```

来并行处理这些URL。

每次重新运行代码前 最好先清楚.txt文件。
```bash
rm *.txt
```

## 潜力

我还在尝试嵌入组件的图片。这些视觉嵌入可以作为属性添加到组件节点中。
由于我们是通过文本嵌入进行搜索，目前只有一种适合这个任务的模型——CLIP。
如果我们要使用CLIP模型，我们需要使用与CLIP文本模型相同的文本处理模型来处理文本嵌入。
此外，图像则需要使用CLIP的视觉模型进行嵌入。