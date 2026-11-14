# 01 — Document Loaders (`pipeline/ingestion/strategies/loaders.py`)

## Overview

The loader module is the first stage of the ingestion pipeline. Its responsibility is to read raw source files from disk and standardize them into LangChain `Document` objects (`page_content` + `metadata`) so downstream stages (chunking and embedding) remain decoupled from file formats.

## Module Design

Rather than instantiating LangChain loaders directly inside `ingest.py`, `loaders.py` follows a **Strategy + Dispatcher pattern**:

1. **Individual Strategy Functions:** Encapsulate loader-specific initialization and defaults (e.g., `load_text`).
2. **Static Type Guard (`LoaderStrategy`):** Uses `typing.Literal['text']` so IDEs and static type checkers flag invalid strategy names before runtime.
3. **Unified Dispatcher (`get_documents`):** Maps strategy keys to their corresponding loader functions and raises a clear `ValueError` if an unsupported strategy string is passed at runtime.

## Function Reference

### `load_text(file_path: str, encoding: str = "utf-8") -> list[Document]`
Loads a single plain-text (`.txt`) or Markdown (`.md`) file into memory using `langchain_community.document_loaders.TextLoader`.

* **Parameters:**
  * `file_path` (`str`): Path to the target text file.
  * `encoding` (`str`, optional): Character encoding used to read the file. Defaults to `"utf-8"`.
* **Returns:** `list[Document]` — A single-element list containing the file's text in `page_content` and `{"source": file_path}` in `metadata`.

### `get_documents(source_path: str, strategy: LoaderStrategy = "text") -> list[Document]`
Central entry point called by `ingest.py` to load documents using the requested strategy.

* **Parameters:**
  * `source_path` (`str`): Path to the input file.
  * `strategy` (`LoaderStrategy`, optional): Strategy identifier (`"text"`). Defaults to `"text"`.
* **Returns:** `list[Document]`
* **Raises:** `ValueError` if `strategy` is not registered in the internal `loaders` dictionary.

## Integration with `ingest.py`

`pipeline/ingestion/ingest.py` calls `get_documents` inside `ingest()` and logs the loaded document count:

    from strategies.loaders import LoaderStrategy, get_documents

    docs = get_documents(source_path="path/to/file.txt", strategy="text")

## Planned Extensions

* `load_directory`: Batch-loading multi-format folders (`.txt`, `.md`, `.pdf`, `.csv`, `.docx`) via `DirectoryLoader`.
* `load_unstructured`: Layout-aware parsing for complex documents via `UnstructuredLoader`.