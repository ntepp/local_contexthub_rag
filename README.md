# local_contexthub_rag

`local_contexthub_rag` is a Retrieval Augmented Generation (RAG) application that allows you to ask questions about individual web pages. It uses local Language Models (LLMs) via Ollama (`deepseek-r1`), `nomic-embed-text` for embeddings, and Qdrant vector storage to provide contextual and relevant answers.

## Features

* **Single Web Page Loading:** Retrieves content from a given URL using `WebBaseLoader`.
* **Local Language Models:** Utilizes local LLMs via Ollama (`deepseek-r1`) to generate responses.
* **Nomic Embeddings:** Generates embeddings using `nomic-embed-text` for efficient vector search.
* **Qdrant Vector Storage:** Stores and retrieves document embeddings for fast semantic search.
* **Redis Caching:** Accelerates response times by storing loaded document sources, eliminating redundant processing.
* **Interactive Interface:** Allows asking multiple questions about the same loaded context.

## LangChain & LangGraph Integration

This project leverages the power of LangChain and LangGraph to create a flexible and efficient RAG pipeline.

* **LangChain:**
    * Used for loading and processing documents from various sources (local files, web pages).
    * Handles text splitting and embedding generation.
    * Provides tools for interacting with vector stores (Qdrant).
* **LangGraph:**
    * Orchestrates the RAG pipeline by defining the steps involved in retrieving relevant documents and generating answers.
    * Allows for the creation of stateful, multi-actor applications, enabling complex interactions with LLMs and vector stores.
    * The project uses LangGraph to define the interaction between the retreival of the context, and the generation of the response by the LLM.
* **LangSmith:**
    * Provides observability and debugging capabilities for the RAG pipeline.
    * Allows for tracking and visualizing the execution of the LangChain and LangGraph components.
    * Helps in identifying bottlenecks and improving the performance of the application.
    * Allows to create feedback datasets to improve the model.

## Prerequisites

* Python 3.9+
* Ollama installed and the `deepseek-r1` and `nomic-embed-text` models downloaded and running locally.
* Redis and Qdrant running, either locally or via Docker.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repo_url>
    cd local_contexthub_rag
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Linux/macOS
    venv\Scripts\activate # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download models using Ollama:**

    ```bash
    ollama pull deepseek-r1 # or your chosen deepseek-r1 model
    ollama pull nomic-embed-text # Download the nomic embed text model
    ```
    You can add your custom model by setting the variable `LLM_MODEL_NAME='deepseek-r1'` in .env
5. **Start Ollama, Redis, and Qdrant:**
   *Ollama must be running locally. Redis and Qdrant can be run locally or via docker.*
    ```bash
    docker-compose up #If you are using docker for redis and qdrant.
    ```

## Usage

### Local Execution

1.  **Run the application:**

To interact with command line

 ```bash
 python -m src.main
 ```

To Interact with Swagger

 ```bash
uvicorn src.app:app
 ```

2.  **Enter a URL or local path:**

* The application will prompt you to enter a URL or a local path.
* You can enter `exit` to quit.

3.  **Ask questions:**

* After loading a source, you can ask questions about its content.
* Enter `set source` to load a new source, or `exit` to quit.


## Documentation and Custom Inputs

This project is primarily based on the LangChain RAG tutorials found here: [https://python.langchain.com/docs/tutorials/rag/](https://python.langchain.com/docs/tutorials/rag/).

**Custom Inputs and Modifications:**

* **Local LLMs with Ollama:** Instead of using cloud-based LLMs, this project utilizes local LLMs served by Ollama, specifically the `deepseek-r1` model. This allows for offline processing and greater control over the LLM.
* **Nomic Embeddings:** The project uses `nomic-embed-text` for generating embeddings, providing an alternative to other embedding models.
* **Redis Caching:** Redis is implemented to cache loaded document sources, significantly improving performance for repeated queries.
* **Interactive Source Loading:** The user can dynamically load new sources using the `set source` command without restarting the application, enhancing usability.
* **Focused Web Loading:** The application uses WebBaseLoader with a SoupStrainer to focus the scraping to the main content of a webpage.
* **Separate source and question steps:** the source is loaded, and then the user is prompted for question.


## Configuration

* **LLM Models:** LLM models (deepseek-r1) are configured in `src/llm/llm_chain.py`.
* **Embeddings:** Embeddings (`nomic-embed-text`) are configured in `src/vector_store/embeddings.py`.
* **Vector Storage:** Qdrant vector storage is configured in `src/vector_store/store.py`.
* **Redis Caching:** Redis caching is configured in `src/utils/cache.py`.


## Project Structure

The project structure is organized as follows:

```
local_contexthub_rag/
├── src/
│   ├── cache/                 # Caching module
│   │   ├── base.py            # Base caching abstract classes
│   │   ├── factory.py         # Factory for creating cache strategies
│   │   └── redis_cache.py     # Redis-specific caching implementation
│   │
│   ├── data_loading/          # Data loading strategies
│   │   ├── abstract_loader.py # Abstract base loader
│   │   ├── pdf_loader.py      # PDF document loader
│   │   ├── text_splitter.py   # Text splitting utility
│   │   ├── webpage_loader.py  # Webpage loading strategy
│   │   └── website_loader.py  # Website crawling loader
│   │
│   ├── llm/                   # Language Model module
│   │   ├── llm_chain.py       # LLM configuration and chaining
│   │   └── rag_pipeline.py    # RAG pipeline implementation
│   │
│   ├── utils/                 # Utility modules
│   │   └── source_type.py     # Source type detection utilities
│   │
│   ├── vector_store/          # Vector storage module
│   │   ├── __init__.py        # Package initialization
│   │   ├── base.py            # Base vector store abstract classes
│   │   ├── embeddings.py      # Embedding model configuration
│   │   ├── factory.py         # Factory for vector store creation
│   │   ├── in_memory.py       # In-memory vector store implementation
│   │   └── qdrant.py          # Qdrant vector store implementation
│   │
│   ├── app.py                 # Main application entry point
│   └── main.py                # Command-line interface
│
├── .env                       # Environment variables configuration
├── .gitignore                 # Git ignore file
├── requirements.txt           # Python project dependencies
└── README.md                  # Project documentation
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License — see the [MIT License](https://opensource.org/licenses/MIT) page for details.  

## Contributing

Contributions are welcome! Feel free to fork the repository, submit issues, and create pull requests.

By contributing, you agree that your contributions will be licensed under the same MIT License.
