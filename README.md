# GraphBuilder 🚀

**An Advanced Knowledge Graph Builder for Web Content**

Build intelligent knowledge graphs from web pages and documents using state-of-the-art LLM models and Neo4j database. Originally developed for DFRobot Co. to enhance their RAG (Retrieval-Augmented Generation) system.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.21%2B-green)](https://neo4j.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🎯 Vision**: Transform unstructured web content into structured knowledge graphs for intelligent information retrieval and analysis.

**Languages**: [English](README.md) | [中文](README_ZH.md)

## ✨ Key Features

- 🌐 **Multi-source Processing**: URLs, JSON files, and local documents
- 🤖 **LLM Integration**: Support for Azure OpenAI, OpenAI, and other models
- 🕷️ **Smart Web Crawling**: Parallel crawling with rate limiting and domain filtering
- 📊 **Neo4j Integration**: Direct integration with Neo4j graph database
- 🔧 **CLI Interface**: Comprehensive command-line interface for all operations
- ⚙️ **Configurable**: Environment-based configuration management
- 📝 **Advanced Logging**: Structured logging with file rotation and colors
- 🚨 **Error Handling**: Comprehensive error handling and recovery
- 🔍 **Input Validation**: Robust validation for URLs, data, and configurations
- 🎨 **Visual Embeddings**: CLIP-based image processing (experimental)

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/VincentPit/GraphBuilder.git
cd GraphBuilder

# 2. Set up environment
conda env create -f environment.yml
conda activate graph
pip install -r condaenv.rnehk3uw.requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your settings

# 4. Test the setup
python demo.py

# 5. Process your first URL
python cli.py url https://www.dfrobot.com
```

## 📦 Installation

### Prerequisites

- **Python 3.8+** with conda/pip
- **Neo4j 5.21+** database server
- **LLM API access** (Azure OpenAI, OpenAI, or others)
- **CUDA GPU** (optional, for faster processing)

### Step-by-Step Installation

#### 1. Clone and Setup Python Environment

```bash
git clone https://github.com/VincentPit/GraphBuilder.git
cd GraphBuilder

# Create conda environment
conda env create -f environment.yml
conda activate graph

# Install Python dependencies
pip install -r condaenv.rnehk3uw.requirements.txt
```

#### 2. Install and Configure Neo4j

**Option A: Docker (Recommended)**
```bash
docker run \
    --name neo4j-graphbuilder \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -v neo4j_data:/data \
    -v neo4j_logs:/logs \
    -v neo4j_import:/var/lib/neo4j/import \
    -v neo4j_plugins:/plugins \
    --env NEO4J_AUTH=neo4j/your_password \
    --env NEO4J_PLUGINS='["apoc"]' \
    --env NEO4J_dbms_security_procedures_unrestricted=apoc.* \
    --env NEO4J_dbms_security_procedures_allowlist=apoc.* \
    neo4j:5.21
```

**Option B: System Installation**
```bash
# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 5' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j=1:5.21.0

# Configure APOC plugin
sudo wget -P /var/lib/neo4j/plugins/ \
    https://github.com/neo4j/apoc/releases/download/5.21.0/apoc-5.21.0-core.jar

# Edit configuration
sudo nano /etc/neo4j/neo4j.conf
```

**Neo4j Configuration (neo4j.conf)**:
```bash
# Enable APOC procedures
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.*

# Memory settings (adjust based on your system)
server.memory.heap.initial_size=1G
server.memory.heap.max_size=2G
server.memory.pagecache.size=1G
```

#### 3. Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit the .env file with your settings
nano .env
```

**Required Configuration (.env)**:
```bash
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# LLM Configuration (choose one)
# For Azure OpenAI
LLM_MODEL_NAME=azure_ai_gpt_4o
LLM_MODEL_CONFIG_azure_ai_gpt_4o=gpt-4o,https://your-endpoint.openai.azure.com/,your-api-key,2024-02-01

# For OpenAI
# LLM_MODEL_NAME=openai-gpt-4o
# OPENAI_API_KEY=your_openai_api_key

# Crawler Settings
MAX_CRAWL_LIMIT=10
MAX_WORKERS=5
ALLOWED_DOMAINS=dfrobot

# Processing Settings
CHUNK_SIZE=200
CHUNK_OVERLAP=20
```

#### 4. Verify Installation

```bash
# Test database connection
python cli.py config

# Run demo to verify all components
python demo.py

# Test with a simple URL
python cli.py url https://www.dfrobot.com --output test_results.json
```

## 📊 Configuration

GraphBuilder uses environment variables for configuration. All settings can be customized in your `.env` file:

### Database Settings
```bash
NEO4J_URI=bolt://localhost:7687      # Neo4j connection URI
NEO4J_USER=neo4j                     # Database username
NEO4J_PASSWORD=your_password         # Database password
NEO4J_DATABASE=neo4j                 # Database name
```

### LLM Settings
```bash
LLM_MODEL_NAME=azure_ai_gpt_4o       # Model identifier
# Azure OpenAI format: model,endpoint,key,version
LLM_MODEL_CONFIG_azure_ai_gpt_4o=gpt-4o,https://your-endpoint.openai.azure.com/,your-api-key,2024-02-01
```

### Crawler Settings
```bash
MAX_CRAWL_LIMIT=10                   # Maximum URLs to process
MAX_WORKERS=5                        # Concurrent worker threads
CRAWL_DELAY=1                        # Delay between requests (seconds)
ALLOWED_DOMAINS=dfrobot              # Comma-separated allowed domains
```

### Processing Settings
```bash
CHUNK_SIZE=200                       # Text chunk size (tokens)
CHUNK_OVERLAP=20                     # Overlap between chunks
MAX_CHUNKS_ALLOWED=1000              # Maximum chunks per document
```

## 🎯 Usage

GraphBuilder provides multiple interfaces for different use cases:

### 1. Command Line Interface (Recommended)

#### Process Single URL
```bash
# Basic URL processing
python cli.py url https://www.dfrobot.com

# With custom parameters
python cli.py url https://www.dfrobot.com \
    --allowed-nodes "Product,Company,Technology" \
    --allowed-relationships "MANUFACTURES,DEVELOPS" \
    --model azure_ai_gpt_4o \
    --output results.json
```

#### Crawl Multiple URLs
```bash
# Crawl starting from multiple URLs
python cli.py crawl https://www.dfrobot.com https://www.dfrobot.com/blog \
    --max-urls 20 \
    --max-workers 3

# Advanced crawling with filtering
python cli.py crawl https://www.dfrobot.com \
    --max-urls 50 \
    --allowed-nodes "Product,Company,Person,Technology" \
    --allowed-relationships "MANUFACTURES,DEVELOPS,WORKS_FOR"
```

#### Process JSON Data
```bash
# Process from JSON file
python cli.py json data/sample.json

# Example JSON format:
cat > sample.json << EOF
{
  "urls": ["https://www.dfrobot.com/product-1.html"],
  "allowed_nodes": ["Product", "Company", "Technology"],
  "allowed_relationships": ["MANUFACTURES", "DEVELOPS"],
  "model": "azure_ai_gpt_4o"
}
EOF
```

#### Monitor Status
```bash
# Check overall status
python cli.py status

# Check specific document status
python cli.py status --file-name "https://www.dfrobot.com"

# Reset crawler state
python cli.py reset-crawler

# View configuration
python cli.py config
```

### 2. Programmatic Usage

```python
from app import app
from logger_config import setup_logging

# Setup logging
setup_logging(log_level="INFO")

# Process single URL
result = app.process_single_url(
    url="https://www.dfrobot.com/product-arduino-uno.html",
    allowed_nodes=["Product", "Company", "Technology", "Feature"],
    allowed_relationships=["MANUFACTURES", "HAS_FEATURE", "COMPATIBLE_WITH"]
)

print(f"Processing result: {result}")

# Crawl multiple URLs
result = app.crawl_and_process_urls(
    start_urls=["https://www.dfrobot.com"],
    allowed_nodes=["Product", "Company"],
    allowed_relationships=["MANUFACTURES"],
    max_workers=3
)

# Process JSON data
json_data = {
    "urls": ["https://www.dfrobot.com/category-arduino.html"],
    "allowed_nodes": ["Product", "Category", "Brand"],
    "allowed_relationships": ["BELONGS_TO", "MANUFACTURED_BY"]
}
result = app.process_from_json_data(json_data)

# Always shutdown gracefully
app.shutdown()
```

### 3. Legacy Scripts (Backward Compatibility)

For users familiar with the original interface:

```bash
# Improved main scripts
python main_improved.py           # Enhanced URL processing
python main_json_improved.py      # Enhanced JSON processing

# Original scripts (still supported)
python main_url.py               # Original URL processing
python main_json.py              # Original JSON processing
python main_para.py              # Parallel processing
```

## 🏗️ Architecture

GraphBuilder follows a modern layered architecture:

```
┌─────────────────────────────────────────────────────┐
│                CLI Interface                        │
├─────────────────────────────────────────────────────┤
│              Application Layer                      │
│                   (app.py)                          │
├─────────────────────────────────────────────────────┤
│                Services Layer                       │
│  ┌─────────────┬─────────────┬─────────────────────┐ │
│  │ LLM Service │ Crawler     │ Document Processor  │ │
│  │             │ Service     │                     │ │
│  └─────────────┴─────────────┴─────────────────────┘ │
├─────────────────────────────────────────────────────┤
│              Database Layer                         │
│  ┌─────────────────────┬─────────────────────────┐   │
│  │ Connection Manager  │ Repositories            │   │
│  └─────────────────────┴─────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│              Data Models                            │
│  ┌─────────────┬─────────────┬─────────────────────┐ │
│  │ SourceNode  │ ChunkDoc    │ Entities            │ │
│  └─────────────┴─────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Core Components

- **Application Layer**: Orchestrates all operations
- **Services Layer**: Business logic for different operations  
- **Database Layer**: Data persistence and retrieval
- **Data Models**: Type-safe entity definitions
- **Configuration**: Environment-based settings
- **Utilities**: Validation, helpers, and common functions

## 📚 API Reference

### Main Application (`app.py`)

```python
class GraphBuilderApp:
    def process_single_url(url: str, allowed_nodes: List[str] = None, 
                          allowed_relationships: List[str] = None) -> Dict
    def crawl_and_process_urls(start_urls: List[str], **kwargs) -> Dict
    def process_from_json_data(json_data: Dict) -> Dict
    def get_processing_status(file_name: str = None) -> Dict
    def reset_crawler() -> Dict
```

### Services

```python
# LLM Service
llm_service.generate_graph_documents(chunk_documents, allowed_nodes, allowed_relationships)

# Crawler Service  
crawler_service.crawl_urls_parallel(start_urls, process_callback, max_workers)

# Document Service
document_processor.process_url_to_graph(url, allowed_nodes, allowed_relationships)
```

## 💡 Examples

### Example 1: E-commerce Product Analysis
```bash
python cli.py url https://www.dfrobot.com/product-arduino-uno.html \
    --allowed-nodes "Product,Brand,Category,Feature,Price,Specification" \
    --allowed-relationships "MANUFACTURED_BY,BELONGS_TO,HAS_FEATURE,PRICED_AT" \
    --output product_analysis.json
```

### Example 2: Company Knowledge Base
```bash
python cli.py crawl https://www.dfrobot.com \
    --max-urls 100 \
    --allowed-nodes "Company,Product,Technology,Person,Location,Event" \
    --allowed-relationships "DEVELOPS,MANUFACTURES,LOCATED_IN,PARTICIPATES_IN"
```

### Example 3: Technical Documentation
```python
result = app.process_single_url(
    url="https://www.dfrobot.com/wiki/arduino-tutorials",
    allowed_nodes=["Tutorial", "Component", "Code", "Concept"],
    allowed_relationships=["TEACHES", "USES", "IMPLEMENTS", "EXPLAINS"]
)
```

## 🧪 Advanced Features

### Visual Embeddings (Experimental)

GraphBuilder supports experimental visual embeddings using CLIP:

```python
# Enable image processing
from ImageEmbed.clip import process_images

# Process images from web pages
images = process_images(url="https://www.dfrobot.com/products")
```

**Note**: Visual embeddings require switching to CLIP's text model for consistency.

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check Neo4j status
   sudo systemctl status neo4j
   
   # Verify connection settings
   python cli.py config
   ```

2. **LLM API Errors**
   ```bash
   # Verify API configuration
   echo $LLM_MODEL_CONFIG_azure_ai_gpt_4o
   
   # Test with minimal example
   python demo.py
   ```

3. **Memory Issues**
   ```bash
   # Reduce chunk size and worker count
   export CHUNK_SIZE=100
   export MAX_WORKERS=2
   ```

4. **Permission Errors**
   ```bash
   # Check file permissions
   chmod +x *.py
   
   # Verify log directory
   mkdir -p logs
   ```

### Debug Mode

Enable detailed logging:
```bash
python cli.py url https://example.com --log-level DEBUG
```

Check logs:
```bash
tail -f logs/graphbuilder.log
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black . && isort .

# Type checking
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DFRobot Co.** - Original project sponsor
- **llm-graph-builder** - Inspiration and foundation
- **Neo4j Community** - Graph database platform
- **LangChain** - LLM integration framework
- **Contributors** - All who helped improve this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/VincentPit/GraphBuilder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/VincentPit/GraphBuilder/discussions)
- **Documentation**: [Wiki](https://github.com/VincentPit/GraphBuilder/wiki)

---

**Made with ❤️ for the open source community**