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

    Raw File / Directory (.txt, .md, .pdf, .csv, .docx) ──► loaders.py ──► list[Document]

- **Loaders (`ingestion/strategies/loaders.py`):** Implements single-file text (`TextLoader`), multi-format directory (`DirectoryLoader`), and layout-aware complex document ingestion (`UnstructuredLoader` via API), routed through the `get_documents` dispatcher.
- **Chunkers & Embedders:** Planned for upcoming milestones.

## Setup & Usage

1. **Activate the project virtual environment** from the repository root:

       # Windows
       .venv\Scripts\activate

       # macOS / Linux
       source .venv/bin/activate

2. **Install required dependencies:**

       pip install -r requirements.txt

3. **Configure environment variables** by copying `.env.example` to `.env` in the repository root and adding your API key (required for `unstructured` and `.docx` directory loading):

       # Windows
       copy .env.example .env

       # macOS / Linux
       cp .env.example .env

   Then update `UNSTRUCTURED_API_KEY` inside `.env`:

       UNSTRUCTURED_API_KEY=your_api_key_here

4. **Run the ingestion entry point** from anywhere in the repository (`ingest.py` resolves paths from `PROJECT_ROOT`):

       python pipeline/ingestion/ingest.py

   *(Uncomment or add your target test call inside `main()` in `ingest.py` before running.)*

## Component Documentation

- [01 - Document Loaders](docs/01-loaders.md): Architecture, function signatures, type safety (`LoaderStrategy`), and usage examples for `loaders.py`.