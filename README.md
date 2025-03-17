# local_contexthub_rag

`local_contexthub_rag` is a Retrieval Augmented Generation (RAG) application that allows you to ask questions about individual web pages. It uses local Language Models (LLMs) via Ollama (`deepseek-r1`), `nomic-embed-text` for embeddings, and Qdrant vector storage to provide contextual and relevant answers.

## Features

* **Single Web Page Loading:** Retrieves content from a given URL using `WebBaseLoader`.
* **Local Language Models:** Utilizes local LLMs via Ollama (`deepseek-r1`) to generate responses.
* **Nomic Embeddings:** Generates embeddings using `nomic-embed-text` for efficient vector search.
* **Qdrant Vector Storage:** Stores and retrieves document embeddings for fast semantic search.
* **Redis Caching:** Accelerates response times by storing loaded document sources, eliminating redundant processing.
* **Interactive Interface:** Allows asking multiple questions about the same loaded context.

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

5. **Start Ollama, Redis, and Qdrant:**
   *Ollama must be running locally. Redis and Qdrant can be run locally or via docker.*
    ```bash
    docker-compose up #If you are using docker for redis and qdrant.
    ```

## Usage

### Local Execution

1.  **Run the application:**

 ```bash
 python -m src.main
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

```
local_contexthub_rag/
├── src/
│   ├── data_loading/
│   │   ├── loaders.py
│   │   ├── text_splitter.py
│   ├── llm/
│   │   ├── llm_chain.py
│   ├── rag/
│   │   ├── rag_pipeline.py
│   ├── vector_store/
│   │   ├── embeddings.py
│   │   ├── store.py
│   ├── utils/
│   │   ├── cache.py
│   ├── main.py
├── models/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Contributions

Contributions are welcome! Feel free to submit pull requests to improve the project.
