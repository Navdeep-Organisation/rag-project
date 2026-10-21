import os
import warnings

# Suppress deprecation warnings from langchain_community
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import TextLoader , DirectoryLoader # pyright: ignore
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()


def load_documents(docs_path = "docs"):
    """load all text files from the docs directory"""
    print(f"Loading documents from {docs_path}...")

    # Check if document exists
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory {docs_path} does not exixts . please check and add your files")

    # Load all txt files from the docs directory
    loader = DirectoryLoader(
        path=docs_path,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()

    """
    documents = [
        Document(
            page_content = "all about a text file you have give like content of google.txt",
            metadata={'source':'docs/google.txt'}
            ),
        Document(
            page_content = "all about a text file you have give like content of microsoft.txt",
            metadata={'source':'docs/microsoft.txt'}
            )
    ]
    """

    if len(documents) == 0:
        raise FileNotFoundError(f"No .txt file in {docs_path}. plese add your files.")

    for i,doc in enumerate(documents[:2]):# show first 2 documents
        print(f"\nDocument{i+1}:")
        print(f" sourse: {doc.metadata['source']}")
        print(f" content length : {len(doc.page_content)} characters")
        print(f" content preview : {doc.page_content[:100]}...")
        print(f" metadata : {doc.metadata}")

    return documents


def split_documents(documents,chunk_size = 800, chunk_overlap = 0):
    """Splits document into smaller chunks with overlap"""
    print("splitting documents into chunks...")

    text_splitter = CharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)

    if chunks:
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n---chunk{i+1}---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("_"*50)

        if len(chunks) > 5:
            print(f"\n... and {len(chunks)-5} more chunks")

    return chunks 


def create_vector_store(chunks,persist_directory = "db/chroma_db"):
    """create and presist ChromaDB vector store"""
    print("cereating embedding and storing in Chromadb")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # creating ChromaDb vector store
    print("--- creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space":"cosine"}
    )
    print("---Fineshed creating vector store ---")
    
    print(f"vector store created and saved to {persist_directory}")
    return vectorstore


def main():
    print("main function ")

    ##laoding files
    documents = load_documents(docs_path="docs")

    ##Chunking the files
    chunks = split_documents(documents)

    ## embedding anf storing in vector db 
    vectorstore = create_vector_store(chunks)


if __name__ == "__main__":
    main()
