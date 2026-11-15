"""Orchestrator and entry point for the document ingestion pipeline."""

from pathlib import Path
from typing import Any
from langchain_core.documents import Document
from strategies.loaders import LoaderStrategy, get_documents

# Anchor to repo root (rag-project/) regardless of terminal working directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]  


def ingest(
    source_path: str | Path,
    loader_strategy: LoaderStrategy = "text",
    **loader_kwargs: Any,
) -> list[Document]:
    """Runs the ingestion pipeline stages for a given source path."""
    docs = get_documents(
        source_path=str(source_path),
        strategy=loader_strategy,
        **loader_kwargs,
    )
    print(f"Loaded {len(docs)} document(s) using '{loader_strategy}' strategy.")
    return docs


def main() -> None:
    """
    Entry-point for Ingestion Pipeline.
    Call the intended strategies below to test each one.
    """
    sample_dir = PROJECT_ROOT / "sample_data"

    # 1. Single plain-text / Markdown file
    # ingest(source_path=sample_dir / "Google.txt", loader_strategy="text")

    # 2. Multi-format directory (.txt, .md, .pdf, .csv, .docx)
    # ingest(source_path=sample_dir, loader_strategy="directory")

    # 3. Complex document via Unstructured API (default: mode="single", partition_strategy="auto")
    # ingest(source_path=sample_dir / "sample.pdf", loader_strategy="unstructured")

    # 4. Unstructured API with custom partitioning options
    # docs = ingest(
    #     source_path=sample_dir / "sample5.pdf",
    #     loader_strategy="unstructured",
    #     mode="elements",
    #     partition_strategy="hi_res",
    # )
    
    # Quick inspection of loaded document metadata and content preview
    # for i, doc in enumerate(docs):
    #     print(f"[{i}] category={doc.metadata.get('category')} | page={doc.metadata.get('page_number')}")
    #     print(f"    content={doc.page_content[:80]!r}\n")
    pass


if __name__ == "__main__":
    main()