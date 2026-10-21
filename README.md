# RAG Project

A Retrieval-Augmented Generation (RAG) pipeline built for a university project.
It splits PDFs into chunks, stores them in a vector database, retrieves the most
relevant chunks for a question, splits long prompts into chunks, and sends them to
a language model to produce an answer.

## Pipeline

```
PDF ──► load text ──► chunk ──► embed ──► vector DB
                                             │
question ──► embed ──► retrieve top-k chunks ┘
                           │
                           ▼
              build prompt ──► prompt chunking ──► LLM ──► answer
```

