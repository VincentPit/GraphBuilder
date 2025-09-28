# Migration Guide: Old Code → Restructured GraphBuilder

This guide helps you understand how to migrate from the old GraphBuilder structure to the new, improved version.

## 📋 Overview

The restructured GraphBuilder provides the same functionality with significant improvements in:
- **Architecture**: Better separation of concerns
- **Error Handling**: Comprehensive error handling
- **Configuration**: Centralized configuration management
- **Logging**: Structured logging with file rotation
- **Type Safety**: Type hints throughout
- **Maintainability**: Cleaner, more maintainable code

## 🔄 Code Migration Examples

### 1. Database Access

**Old Code** (`dbAccess.py`):
```python
from dbAccess import graphDBdataAccess
from shared.common_fn import create_graph_database_connection

graph = create_graph_database_connection()
db_access = graphDBdataAccess(graph)
db_access.create_source_node(source_node)
```

**New Code**:
```python
from database.connection import db_manager
from database.repositories import SourceNodeRepository

graph = db_manager.get_graph()
repo = SourceNodeRepository(graph)
repo.create(source_node)
```

### 2. Source Node Creation

**Old Code**:
```python
from entities.source_node import sourceNode

source_node = sourceNode()
source_node.file_name = "example.txt"
source_node.status = "New"
source_node.created_at = datetime.now()
```

**New Code**:
```python
from entities.source_node import SourceNode, SourceStatus

source_node = SourceNode(
    file_name="example.txt",
    status=SourceStatus.NEW
    # created_at is automatically set
)
```

### 3. LLM Operations

**Old Code** (`llm.py`):
```python
from llm import generate_graphDocuments, get_llm

model = get_llm("azure_ai_gpt_4o")
graph_docs = generate_graphDocuments(model, graph, chunks, nodes, relationships)
```

**New Code**:
```python
from services.llm_service import llm_service

graph_docs = llm_service.generate_graph_documents(
    chunk_documents=chunks,
    allowed_nodes=nodes,
    allowed_relationships=relationships
)
```

### 4. Web Crawling

**Old Code** (`main_url.py`):
```python
# Global variables and manual state management
visited = set()
processed_urls = set()
MAX_CRAWL_LIMIT = 2

def crawl_urls_in_parallel(graph, model, allowed_nodes, allowed_relationship, delay=1, max_workers=5):
    # Complex manual implementation
    pass
```

**New Code**:
```python
from services.crawler_service import crawler_service
from app import app

result = app.crawl_and_process_urls(
    start_urls=["https://example.com"],
    allowed_nodes=["Product", "Company"],
    allowed_relationships=["MANUFACTURES"]
)
```

### 5. Document Processing

**Old Code** (`processing.py`):
```python
from processing import CreateChunksofDocument, create_source_node_graph_dfrobot_url

processor = CreateChunksofDocument(pages, graph)
chunks = processor.split_file_into_chunks()
```

**New Code**:
```python
from services.document_service import document_processor

chunks = document_processor.split_documents_into_chunks(documents)
```

### 6. Configuration

**Old Code**:
```python
# Hardcoded values scattered throughout
MAX_CRAWL_LIMIT = 2
VISITED_FILE = 'record/visited_urls.json'
```

**New Code**:
```python
from config import config

max_limit = config.crawler.max_crawl_limit
visited_file = config.crawler.visited_urls_file
```

### 7. Logging

**Old Code**:
```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Processing started")
```

**New Code**:
```python
from logger_config import logger

logger.info("Processing started")
# Automatic file rotation, colors, structured format
```

### 8. Error Handling

**Old Code**:
```python
try:
    # some operation
    pass
except Exception as e:
    print(f"Error: {e}")
```

**New Code**:
```python
from exceptions import ProcessingError
from logger_config import logger

try:
    # some operation
    pass
except Exception as e:
    logger.error(f"Processing failed: {e}")
    raise ProcessingError(f"Operation failed: {e}") from e
```

## 🗂️ File Mapping

| Old File | New Location | Purpose |
|----------|-------------|---------|
| `main_url.py` | `main_improved.py` + `app.py` | Main URL processing |
| `main_json.py` | `main_json_improved.py` + `app.py` | JSON processing |
| `dbAccess.py` | `database/repositories.py` | Database operations |
| `processing.py` | `services/document_service.py` | Document processing |
| `llm.py` | `services/llm_service.py` | LLM operations |
| `entities/source_node.py` | `entities/source_node.py` | Source node (improved) |
| `shared/common_fn.py` | `utils/helpers.py` | Common functions |
| `shared/constants.py` | `config.py` + `shared/constants.py` | Configuration |

## 🚀 Running the New Code

### Using the CLI (Recommended)

```bash
# Process single URL
python cli.py url https://www.dfrobot.com

# Crawl multiple URLs  
python cli.py crawl https://www.dfrobot.com --max-urls 10

# Process JSON data
python cli.py json data/sample.json

# Check status
python cli.py status
```

### Using the Improved Main Scripts

```bash
# URL processing
python main_improved.py

# JSON processing
python main_json_improved.py
```

### Programmatic Usage

```python
from app import app

# Single URL
result = app.process_single_url("https://www.dfrobot.com")

# Multiple URLs
result = app.crawl_and_process_urls(["https://www.dfrobot.com"])

# JSON data
result = app.process_from_json_data(json_data)
```

## ⚙️ Configuration Migration

### Old Approach
```python
# Scattered hardcoded values
MAX_CRAWL_LIMIT = 2
VISITED_FILE = 'record/visited_urls.json'
```

### New Approach
Create `.env` file:
```bash
MAX_CRAWL_LIMIT=10
VISITED_URLS_FILE=record/visited_urls.json
NEO4J_URI=bolt://localhost:7687
LLM_MODEL_NAME=azure_ai_gpt_4o
```

## 🔍 Key Benefits of Migration

1. **Better Error Handling**: Specific exceptions and graceful error recovery
2. **Configuration Management**: Environment-based configuration
3. **Logging**: Structured logging with file rotation and colors
4. **Type Safety**: Type hints for better IDE support and fewer bugs
5. **Maintainability**: Modular design makes code easier to maintain
6. **Testing**: Architecture supports better unit testing
7. **Performance**: Improved resource management and parallel processing
8. **Monitoring**: Better progress tracking and status reporting

## 🧪 Testing Your Migration

1. **Run the Demo**:
   ```bash
   python demo.py
   ```

2. **Test Configuration**:
   ```bash
   python cli.py config
   ```

3. **Test URL Processing**:
   ```bash
   python cli.py url https://www.dfrobot.com --output test_results.json
   ```

4. **Check Logs**:
   ```bash
   tail -f logs/graphbuilder.log
   ```

## 🚨 Breaking Changes

1. **Import Paths**: All import paths have changed
2. **Function Signatures**: Some function signatures have changed
3. **Configuration**: Configuration is now environment-based
4. **Error Types**: Custom exceptions instead of generic exceptions
5. **Logging**: New logging format and configuration

## 💡 Tips for Migration

1. **Start with CLI**: Use the CLI to test functionality before programmatic usage
2. **Check Configuration**: Ensure all environment variables are set
3. **Test Incrementally**: Migrate one component at a time
4. **Use Demo Script**: Run the demo to understand new features
5. **Check Logs**: Monitor logs for any issues during migration

## 📞 Support

If you encounter issues during migration:

1. Check the logs in `logs/graphbuilder.log`
2. Run `python cli.py config` to verify configuration
3. Use `python demo.py` to test basic functionality
4. Check the `.env` file for missing configuration

## 🔗 Additional Resources

- [README_IMPROVED.md](README_IMPROVED.md) - Complete documentation
- [demo.py](demo.py) - Demonstration script
- [cli.py](cli.py) - Command-line interface
- [.env.example](.env.example) - Example configuration