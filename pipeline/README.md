# Ingestion & Retrieval Pipeline (`team-pipeline`)

This module handles document loading, chunking, embedding generation, and query-time retrieval for the RAG system.

## Directory Structure

    pipeline/
    ├── README.md
    ├── docs/
    │   └── 01-loaders.md          # Detailed walkthrough of document loading strategies
    └── ingestion/
        ├── ingest.py              # Entry point and orchestrator for the ingestion workflow
        └── strategies/
            ├── __init__.py        # Package marker for strategy modules
            └── loaders.py         # Document loader implementations and dispatcher

## Current Pipeline Stage

    Raw File (.txt / .md) ──► loaders.py (TextLoader) ──► list[Document]

* **Loaders (`ingestion/strategies/loaders.py`):** Currently implements single-file plain-text/Markdown ingestion via `TextLoader`, routed through the `get_documents` dispatcher.
* **Chunkers & Embedders:** Planned for upcoming milestones.

## Setup & Usage

1. **Activate the project virtual environment** from the repository root:

       # Windows
       .venv\Scripts\activate

       # macOS / Linux
       source .venv/bin/activate

2. **Install required dependencies:**

       pip install langchain-core langchain-community

3. **Run the ingestion entry point** from `pipeline/ingestion/`:

       cd pipeline/ingestion
       python ingest.py

   *(Uncomment or add your target test call inside `main()` in `ingest.py` before running.)*

## Component Documentation

* [01 - Document Loaders](docs/01-loaders.md): Architecture, function signatures, type safety (`LoaderStrategy`), and usage examples for `loaders.py`.