# GenAI RAG Assistant

Enterprise-ready Retrieval-Augmented Generation (RAG) backend built with FastAPI, LangChain, ChromaDB, and OpenAI. Designed for modularity, clean code, and precise document-based question answering with source citations.

## Architecture & Theoretical Background

The system combines vector embeddings and large language models to answer user queries grounded in custom documents (e.g., PDF manuals, research papers).

- **Vector Space & Embeddings:** Documents and queries are mapped into a high-dimensional real vector space ($\mathbb{R}^{d}$, where $d = 1536$ for OpenAI embeddings) and projected onto a hyperspace unit sphere.
- **Distance Metric:** Semantic relevance is measured using cosine distance based on the angle between vectors.
- **Hybrid Retrieval:** Combines BM25 (keyword) and vector (semantic) search with equal weights for robust retrieval.
- **Retrieval & Generation:** ChromaDB acts as the vector database retrieving the top-$k$ most similar chunks, while the LLM synthesizes the final response strictly within the provided context.

## Project Structure

```text
GenAI-RAG-Assistant/
├── app/
│   ├── api/
│   │   └── endpoints.py      # FastAPI routers (/upload, /chat)
│   ├── core/
│   │   └── config.py         # Application settings & environment configuration
│   ├── models/
│   │   └── schemas.py        # Pydantic validation models
│   └── services/
│       └── rag_service.py    # Core RAG logic, ChromaDB, and LangChain pipeline
├── tests/
│   ├── conftest.py           # TestClient and PDF upload fixture
│   ├── test_health.py        # Smoke tests
│   ├── test_upload.py        # Upload validation tests
│   ├── test_chat.py          # Chat endpoint tests
│   └── test_e2e.py           # End-to-end RAG test
├── main.py                   # FastAPI application entry point with CORS middleware
├── rag_prototype.py          # CLI prototype script for local testing
├── evaluate.py               # Automated evaluation script (15 domain-specific queries)
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
└── .env.example              # Environment variables template
```



Author
Patrik Madár

GitHub: @zenpeter-123

Email: madarpatrik369@gmail.com
