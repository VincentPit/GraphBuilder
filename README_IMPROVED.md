# GraphBuilder - Restructured and Improved

A restructured and improved version of the GraphBuilder project for building knowledge graphs from web content, with better architecture, error handling, and maintainability.

## 🚀 What's New

### Major Improvements

1. **Better Architecture**: Modular design with clear separation of concerns
2. **Configuration Management**: Centralized configuration with environment variable support
3. **Proper Logging**: Structured logging with file rotation and colored output
4. **Error Handling**: Custom exceptions and comprehensive error handling
5. **Type Safety**: Added type hints throughout the codebase
6. **Data Models**: Improved entity models with validation
7. **Service Layer**: Clean separation between business logic and data access
8. **CLI Interface**: Comprehensive command-line interface
9. **Validation**: Input validation and sanitization
10. **Testing**: Structured for better testability

### New Project Structure

```
GraphBuilder/
├── app.py                     # Main application orchestrator
├── cli.py                     # Command-line interface
├── config.py                  # Configuration management
├── exceptions.py              # Custom exceptions
├── logger_config.py           # Logging configuration
├── main_improved.py           # Improved main script for URL processing
├── main_json_improved.py      # Improved JSON processing script
├── database/                  # Database layer
│   ├── __init__.py
│   ├── connection.py          # Database connection manager
│   └── repositories.py        # Repository pattern for data access
├── entities/                  # Data models
│   ├── __init__.py
│   ├── source_node.py         # Improved source node entity
│   ├── chunk.py               # Chunk document entity
│   └── user_credential.py     # User credentials (unchanged)
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── llm_service.py         # LLM operations
│   ├── crawler_service.py     # Web crawling service
│   └── document_service.py    # Document processing service
├── utils/                     # Utilities
│   ├── __init__.py
│   ├── validators.py          # Validation utilities
│   └── helpers.py             # Helper functions
├── shared/                    # Shared components (kept for compatibility)
└── logs/                      # Log files (auto-created)
```

## 📋 Installation

### Prerequisites

- Python 3.8+
- Neo4j 5.21+
- Conda (recommended for environment management)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/VincentPit/GraphBuilder.git
   cd GraphBuilder
   ```

2. **Create conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate graph
   ```

3. **Install additional requirements**
   ```bash
   pip install -r condaenv.rnehk3uw.requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root:

```bash
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# LLM Configuration
LLM_MODEL_NAME=azure_ai_gpt_4o
LLM_MODEL_CONFIG_azure_ai_gpt_4o=gpt-4o,https://your-endpoint.openai.azure.com/,your-api-key,2024-02-01

# Crawler Configuration
MAX_CRAWL_LIMIT=10
MAX_WORKERS=5
CRAWL_DELAY=1
ALLOWED_DOMAINS=dfrobot

# Processing Configuration
CHUNK_SIZE=200
CHUNK_OVERLAP=20
MAX_CHUNKS_ALLOWED=1000

# Logging
LOG_LEVEL=INFO
```

## 🚀 Usage

### Command Line Interface

The new CLI provides a comprehensive interface for all operations:

```bash
# Process a single URL
python cli.py url https://www.dfrobot.com

# Crawl multiple URLs
python cli.py crawl https://www.dfrobot.com --max-urls 10 --max-workers 3

# Process from JSON file
python cli.py json data/sample.json

# Check processing status
python cli.py status --file-name "https://www.dfrobot.com"

# Reset crawler state
python cli.py reset-crawler

# Show configuration
python cli.py config

# Save results to file
python cli.py url https://www.dfrobot.com --output results.json
```

### Programmatic Usage

```python
from app import app
from logger_config import setup_logging

# Setup logging
setup_logging(log_level="INFO")

# Process single URL
result = app.process_single_url(
    url="https://www.dfrobot.com",
    allowed_nodes=["Product", "Company", "Technology"],
    allowed_relationships=["MANUFACTURES", "DEVELOPS"]
)

# Crawl multiple URLs
result = app.crawl_and_process_urls(
    start_urls=["https://www.dfrobot.com"],
    allowed_nodes=["Product", "Company"],
    allowed_relationships=["MANUFACTURES"]
)

# Process JSON data
json_data = {
    "urls": ["https://www.dfrobot.com/product-1.html"],
    "allowed_nodes": ["Product", "Company"],
    "allowed_relationships": ["MANUFACTURES"]
}

result = app.process_from_json_data(json_data)

# Get status
status = app.get_processing_status()

# Shutdown gracefully
app.shutdown()
```

### Legacy Scripts (Updated)

The original main scripts have been improved but kept for backward compatibility:

```bash
# Improved URL processing
python main_improved.py

# Improved JSON processing
python main_json_improved.py
```

## 🏗️ Architecture

### Key Components

1. **Application Layer** (`app.py`): Main orchestrator that coordinates all services
2. **Services Layer**: Business logic for different operations
   - `llm_service.py`: LLM operations and graph generation
   - `crawler_service.py`: Web crawling with rate limiting
   - `document_service.py`: Document processing and chunking
3. **Database Layer**: Data access with repository pattern
4. **Configuration**: Centralized config management with environment variables
5. **Utilities**: Validation, helpers, and common functions

### Design Principles

- **Separation of Concerns**: Clear boundaries between layers
- **Dependency Injection**: Services receive dependencies through constructors
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Logging**: Structured logging throughout the application
- **Type Safety**: Type hints for better code quality
- **Configuration**: Environment-based configuration
- **Validation**: Input validation and sanitization

## 🔍 Features

### Improved Features

1. **Better Error Handling**: Custom exceptions with detailed error messages
2. **Configurable Logging**: File rotation, colored console output, different log levels
3. **Input Validation**: URL validation, data sanitization, model validation
4. **Rate Limiting**: Configurable delays between requests
5. **Progress Tracking**: Better progress tracking and status reporting
6. **Resource Management**: Proper cleanup and resource management
7. **Parallel Processing**: Improved parallel processing with better error handling
8. **Data Persistence**: Better data persistence and state management

### New Features

1. **CLI Interface**: Comprehensive command-line interface
2. **Configuration Management**: Environment-based configuration
3. **Status Monitoring**: Real-time status monitoring and reporting
4. **Result Export**: Export results to JSON files
5. **Crawler Reset**: Reset crawler state functionality
6. **Model Validation**: Validate LLM model configurations
7. **Backup Management**: Automatic backup file creation

## 🐛 Error Handling

The improved version includes comprehensive error handling:

- **Custom Exceptions**: Specific exceptions for different error types
- **Graceful Degradation**: Continue processing when possible
- **Detailed Logging**: Comprehensive error logging with stack traces
- **Recovery**: Automatic recovery from transient errors
- **Validation**: Input validation to prevent errors

## 📊 Monitoring and Logging

### Logging Features

- **Structured Logging**: Consistent log format across all components
- **File Rotation**: Automatic log file rotation to prevent disk space issues
- **Colored Console**: Color-coded console output for better readability
- **Multiple Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Component Tracking**: Track which component generated each log entry

### Log Files

- **Main Log**: `logs/graphbuilder.log` - Main application log
- **Rotating Files**: Automatic rotation when files exceed 10MB
- **Backup Files**: Keep 5 backup files by default

## 🔒 Security

### Security Improvements

1. **Input Sanitization**: All input data is sanitized to prevent injection
2. **URL Validation**: Strict URL validation before processing
3. **Error Message Sanitization**: Prevent sensitive information leakage
4. **Resource Limits**: Configurable limits to prevent resource exhaustion
5. **Safe File Operations**: Safe file operations with proper error handling

## 🧪 Testing

The restructured code is designed for better testability:

- **Dependency Injection**: Easy to mock dependencies
- **Pure Functions**: Many utility functions are pure and easily testable
- **Error Scenarios**: Better handling of error scenarios
- **Isolated Components**: Components can be tested in isolation

## 📈 Performance

### Performance Improvements

1. **Connection Pooling**: Reuse database connections
2. **Parallel Processing**: Improved parallel processing with better load balancing
3. **Memory Management**: Better memory management and cleanup
4. **Caching**: Internal caching where appropriate
5. **Resource Cleanup**: Proper resource cleanup to prevent leaks

## 🤝 Contributing

1. **Code Style**: Follow PEP 8 and use type hints
2. **Error Handling**: Use custom exceptions appropriately
3. **Logging**: Add appropriate logging statements
4. **Documentation**: Document new features and changes
5. **Testing**: Add tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the original repository for details.

## 🙏 Acknowledgments

- Based on the original GraphBuilder by VincentPit
- Built for DFRobot Co.
- Inspired by llm-graph-builder project

## 🔗 Links

- [Original Repository](https://github.com/VincentPit/GraphBuilder)
- [Chinese README](README_ZH.md)
- [Issues](https://github.com/VincentPit/GraphBuilder/issues)