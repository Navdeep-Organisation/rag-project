"""Orchestrator and entry point for the document ingestion pipeline."""

from langchain_core.documents import Document
from strategies.loaders import(
    LoaderStrategy,
    get_documents
)

def ingest(source_path: str, loader_strategy: LoaderStrategy = "text") -> list[Document]:
    docs = get_documents(source_path=source_path, strategy=loader_strategy)
    print(f"Loaded {len(docs)} document(s).")
    return docs

def main():
    """
    Entry-point for Ingestion Pipeline.
    Call the intended strategies below to test each one.
    """
    # Example test call:
    # ingest(source_path="../../sample_data/Google.txt", loader_strategy="text")
    pass
    

if __name__ == "__main__":
    main()