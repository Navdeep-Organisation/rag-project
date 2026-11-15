# 01 — Document Loaders (`pipeline/ingestion/strategies/loaders.py`)

## Overview

The loader module is the first stage of the ingestion pipeline. Its responsibility is to read raw source files from disk and standardize them into LangChain `Document` objects (`page_content` + `metadata`) so downstream stages (chunking and embedding) remain decoupled from file formats.

## Module Design

Rather than instantiating LangChain loaders directly inside `ingest.py`, `loaders.py` follows a **Strategy + Dispatcher pattern**:

1. **Individual Strategy Functions:** Encapsulate loader-specific initialization, path validation, and defaults (`load_text`, `load_directory`, `load_unstructured`).
2. **Static Type Guards (`Literal` Aliases):** Uses `LoaderStrategy`, `UnstructuredPartitionStrategy`, and `UnstructuredMode` so IDEs and static type checkers flag invalid options before runtime.
3. **Unified Dispatcher (`get_documents`):** Maps strategy keys to their corresponding loader functions, forwards strategy-specific `**loader_kwargs`, and raises a clear `ValueError` if an unsupported strategy string is passed at runtime.

## Function Reference

### `load_text`

```python
def load_text(
    file_path: str,
    encoding: str = "utf-8",
) -> list[Document]
```

Loads a single plain-text (`.txt`) or Markdown (`.md`) file into memory using `langchain_community.document_loaders.TextLoader`.

- **Parameters:**
  * `file_path` (`str`): Path to the target text file.
  * `encoding` (`str`, optional): Character encoding used to read the file. Defaults to `"utf-8"`.
- **Returns:** `list[Document]` — A single-element list containing the file's text in `page_content` and `{"source": file_path}` in `metadata`.
- **Raises:** `FileNotFoundError` if `file_path` does not point to an existing file.

---

### `load_directory`

```python
def load_directory(dir_path: str) -> list[Document]
```

Recursively loads multiple file formats (`.txt`, `.md`, `.pdf`, `.csv`, `.docx`) from a directory by routing each glob pattern to its dedicated loader via `DirectoryLoader` (with `silent_errors=True`).

- **Parameters:**
  * `dir_path` (`str`): Path to the target root directory.
- **Extension Mapping:**
  * `**/*.txt`, `**/*.md` → `TextLoader` (`encoding="utf-8"`)
  * `**/*.pdf` → `PyPDFLoader`
  * `**/*.csv` → `CSVLoader` (`encoding="utf-8"`)
  * `**/*.docx` → `UnstructuredLoader` (`partition_via_api=True`)
- **Returns:** `list[Document]` — Combined documents across all matched files.
- **Raises:** `NotADirectoryError` if `dir_path` does not point to an existing directory.

---

### `load_unstructured`

```python
def load_unstructured(
    file_path: str,
    mode: UnstructuredMode = "single",
    partition_strategy: UnstructuredPartitionStrategy = "auto",
) -> list[Document]
```

Loads complex documents (`.pdf`, `.docx`, `.html`, `.pptx`) with layout-aware partitioning via `langchain_unstructured.UnstructuredLoader` (`partition_via_api=True`).

- **Parameters:**
  * `file_path` (`str`): Path to the target document.
  * `mode` (`Literal["single", "elements"]`, optional): `"single"` combines all content into one `Document`; `"elements"` emits one `Document` per semantic layout element (`Title`, `NarrativeText`, `ListItem`, `Table`, etc.) with element-level metadata (`category`, `page_number`, `parent_id`, `coordinates`). Defaults to `"single"`.
  * `partition_strategy` (`Literal["auto", "fast", "hi_res", "ocr_only"]`, optional): Partitioning strategy used by the Unstructured API (`"auto"` selects `"fast"` for digital text and `"hi_res"` when tables/images are detected). Defaults to `"auto"`.
- **Returns:** `list[Document]`
- **Raises:** `FileNotFoundError` if `file_path` does not point to an existing file.

---

### `get_documents`

```python
def get_documents(
    source_path: str,
    strategy: LoaderStrategy = "text",
    **loader_kwargs: Any,
) -> list[Document]
```

Central entry point called by `ingest.py` to load documents using the requested strategy.

- **Parameters:**
  * `source_path` (`str`): Path to the input file or directory.
  * `strategy` (`Literal["text", "directory", "unstructured"]`, optional): Strategy identifier. Defaults to `"text"`.
  * `**loader_kwargs` (`Any`, optional): Strategy-specific keyword arguments forwarded directly to the underlying loader function (e.g., `encoding`, `mode`, `partition_strategy`).
- **Returns:** `list[Document]`
- **Raises:** `ValueError` if `strategy` is not registered in the internal `loaders` dictionary.

## Execution Modes: Hosted API vs. Local

- **Hosted API (`partition_via_api=True`, Current Default):** Used in `load_unstructured` and `.docx` directory loading via `UNSTRUCTURED_API_KEY` in `.env`. Avoids heavy local vision/OCR binaries (`onnxruntime`, `pdf2image`, Poppler, Tesseract) on Windows while supporting `hi_res` table/layout parsing.
- **Local Lightweight (`partition_via_api=False`, `strategy="fast"`):** Can be used offline without API costs by installing `pdfminer.six` and `python-docx` alongside `langchain-unstructured`.

## Integration with `ingest.py`

`pipeline/ingestion/ingest.py` resolves `PROJECT_ROOT` independently of the terminal working directory, calls `get_documents` inside `ingest()`, and logs the loaded document count:

```python
from strategies.loaders import get_documents

# 1. Single plain-text file
docs = get_documents(source_path="sample_data/Google.txt", strategy="text")

# 2. Mixed-format directory
docs = get_documents(source_path="sample_data", strategy="directory")

# 3. Complex PDF via Unstructured API with element-level hi_res parsing
docs = get_documents(
    source_path="sample_data/sample5.pdf",
    strategy="unstructured",
    mode="elements",
    partition_strategy="hi_res",
)
```