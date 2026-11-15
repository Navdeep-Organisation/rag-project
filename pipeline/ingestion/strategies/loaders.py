"""
    Document loader strategies (text, directory, unstructured) and unified dispatcher.
"""

from pathlib import Path
from typing import Any, Literal
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    CSVLoader,
    PyPDFLoader
)
from langchain_unstructured import UnstructuredLoader

load_dotenv()
LoaderStrategy = Literal["text", "directory", "unstructured"]
UnstructuredPartitionStrategy = Literal["auto", "fast", "hi_res", "ocr_only"]
UnstructuredMode = Literal["single", "elements"]


def load_text(file_path: str, encoding: str = "utf-8") -> list[Document]:
    """Loads a single plain-text or Markdown file."""
    
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Expected a file for load_text, got: {file_path}")

    loader = TextLoader(file_path=str(path), encoding=encoding)
    doc = loader.load()
    return doc


def load_directory(dir_path: str) -> list[Document]:
    """Loads multiple file types (.txt, .md, .pdf, .csv, .docx) from a directory."""
    
    root_dir = Path(dir_path)
    if not root_dir.is_dir():
        raise NotADirectoryError(f"Expected a directory for load_directory, got: {dir_path}")

    loader_map = {
        "**/*.txt": (TextLoader, {"encoding": "utf-8"}),
        "**/*.md": (TextLoader, {"encoding": "utf-8"}),
        "**/*.pdf": (PyPDFLoader, {}),
        "**/*.csv": (CSVLoader, {"encoding": "utf-8"}),
        "**/*.docx": (UnstructuredLoader, {"partition_via_api": True}),
    }

    docs: list[Document] = []
    for glob_pattern, (loader_cls, loader_kwargs) in loader_map.items():
        loader = DirectoryLoader(
            path=str(root_dir),
            glob=glob_pattern,
            loader_cls=loader_cls,
            loader_kwargs=loader_kwargs,
            silent_errors=True,
        )
        docs.extend(loader.load())

    return docs


def load_unstructured(
    file_path: str,
    mode: UnstructuredMode = "single",
    partition_strategy: UnstructuredPartitionStrategy = "auto",
) -> list[Document]:
    """Loads complex files (PDF, DOCX, HTML, PPTX) via langchain_unstructured."""
    
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Expected a file for load_unstructured, got: {file_path}")

    loader = UnstructuredLoader(
        file_path=str(path), 
        mode=mode, 
        strategy=partition_strategy,
        partition_via_api=True
    )
    doc = loader.load()
    return doc

def get_documents(
    source_path: str,
    strategy: LoaderStrategy = "text",
    **loader_kwargs: Any,
) -> list[Document]:
    """Dispatcher that calls the selected loader strategy."""
    loaders = {
        "text": load_text,
        "directory": load_directory,
        "unstructured": load_unstructured,
    }

    if strategy not in loaders:
        raise ValueError(f"Unsupported strategy '{strategy}'. Choose from {list(loaders.keys())}")

    return loaders[strategy](source_path, **loader_kwargs)