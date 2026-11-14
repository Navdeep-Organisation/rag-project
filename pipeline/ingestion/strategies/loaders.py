"""
    Document loader strategies (text, directory, unstructured) and unified dispatcher.
"""

from typing import Literal
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

# a typing.Literal variable to force only available Strategies during Static tpye checking
LoaderStrategy = Literal['text']

def load_text(file_path : str, encoding : str = "utf-8" ) -> list[Document]:
    """Loads a single plain-text or Markdown file."""
    loader = TextLoader(
        file_path=file_path,
        encoding=encoding
    )
    
    docs = loader.load()
    return docs

def get_documents(source_path: str, strategy: LoaderStrategy = "text") -> list[Document]:
    """Dispatcher that calls the selected loader strategy."""
    loaders = {
        "text": load_text
    }
    
    if strategy not in loaders:
        raise ValueError(f"Unsupported strategy '{strategy}'. Choose from {list(loaders.keys())}")
    
    return loaders[strategy](source_path)