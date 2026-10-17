# GenAI RAG Assistant

A modular Retrieval-Augmented Generation (RAG) backend built with FastAPI, LangChain, ChromaDB, and OpenAI. Designed for modularity, clean code, and precise document-based question answering with source citations.

## Architecture & Theoretical Background

The system combines vector embeddings and large language models to answer user queries grounded in custom documents (e.g., PDF manuals, research papers).

- Vector Space & Embeddings: Documents and queries are mapped into a high-dimensional real vector space (R^d, where d = 1536 for OpenAI embeddings) and projected onto a hyperspace unit sphere.
- Distance Metric: Semantic relevance is measured using cosine distance based on the angle between vectors.
- Hybrid Retrieval: Combines BM25 (keyword) and vector (semantic) search with equal weights for robust retrieval.
- Retrieval & Generation: ChromaDB acts as the vector database retrieving the top-k most similar chunks, while the LLM synthesizes the final response strictly within the provided context.

## Project Structure

```
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

## Key Features

### FastAPI Endpoints

- POST /api/v1/upload: Uploads and automatically parses/indexes PDF documents into the persistent ChromaDB vector store.
- POST /api/v1/chat: Handles user queries through the RAG pipeline with configurable retrieval parameters (top_k).

### Vector Search & Persistence

- Powered by ChromaDB using LangChain wrappers and OpenAI embedding models.
- Hybrid search combines BM25 and vector retrieval via EnsembleRetriever with 50/50 weights.

### Robust Anti-Hallucination Behavior

- Built-in validation ensures safe fallbacks when context is missing.
- The LLM answers only based on retrieved context, reducing hallucinations.

### Source Attribution

- Each response includes the source document and page number.

### Automated Testing

- 10 tests with pytest covering smoke, upload, chat, and end-to-end RAG flow.
- Run the automated evaluation script to test 15 domain-specific queries and verify that the RAG pipeline successfully returns responses through the FastAPI test client:
```bash
python evaluate.py

=== RAG SYSTEM AUTOMATED EVALUATION ===
Dokumentum feltöltése és indexelése: project_documentation.pdf...
Sikeres feltöltés és indexelés!


[Test 1/15] Kérdés: Mi a RAG asszisztens alapvető célja a dokumentum szerint?
Válasz: A RAG asszisztens alapvető célja, hogy képes legyen a saját tudástárát ötvözve megadott dokumentumokat figyelembe véve választ adni a felhasználónak....

[Test 2/15] Kérdés: Hány dimenziós valós vektorteret (d) használ az OpenAI modellje?
Válasz: Az OpenAI modellje egyd= 1536 dimenziós valós vektorteret használ....

[Test 3/15] Kérdés: Hova történik a pontok vetítése ebben a vektortér-konstrukcióban?
Válasz: A pontok vetítése az egységgömb felszínére történik ebben a vektortér-konstrukcióban....

[Test 4/15] Kérdés: Pontosan hogyan van definiálva az u és v vektorok közötti távolságmennyiség d(u,v)?
Válasz: Az u és v vektorok közötti távolságmennyiség d(u,v) a következőképpen van definiálva: d(u,v) = ⟨u;v⟩ = cos(θ), ahol θ az u és v vektorok közötti, origóból mért szög....

[Test 5/15] Kérdés: Mitől függ a skaláris szorzat értéke ebben a gömbi távolság-modellben?
Válasz: A skaláris szorzat értéke ebben a gömbi távolság-modellben csak a két vektor bezárt szögétől függ....

[Test 6/15] Kérdés: Mi a pontos célja az embedding modellnek a válaszok és kérdések egységgömbre vetítése mögött?
Válasz: Az embedding modell célja, hogy a válaszokat és kérdéseket úgy helyezze el egy egydimenziós valós vektortérben, hogy meghatározható legyen egy értelmes távolságmetrika a pontok között, mivel a távolságnak a relevanciát szeretnénk megfeleltetni. Az egységgömb felszínére vetítve a pontokat, a modell b...

[Test 7/15] Kérdés: Melyik tudományos cikk foglalkozik a kontrasztív reprezentációtanulással a hiperszférán?
Válasz: A kontrasztív reprezentációtanulással a hiperszférán foglalkozó tudományos cikk a következő: Tongzhou Wang és Phillip Isola. Understanding contrastive representation learning through alignment and uniformity on the hypersphere. CoRR, abs/2005.10242, 2020....

[Test 8/15] Kérdés: A kérdés gömbfelszíni vetületéhez viszonyítva hány legközelebb eső válasz vetületét határozzuk meg?
Válasz: Nem található elegendő információ a dokumentumban....

[Test 9/15] Kérdés: Hogyan osztja le a szerepeket a rendszer a ChromaDB és a nyelvi modell között?
Válasz: Nem található elegendő információ a dokumentumban....

[Test 10/15] Kérdés: Mi a RAG (Retrieval Augmentation Generation) folyamat pontos lépésről lépésre láncolata?
Válasz: A RAG (Retrieval Augmentation Generation) folyamat pontos lépésről lépésre láncolata a következő:

1. Embedding model
2. ChromaDB
3. LLM...

[Test 11/15] Kérdés: Mely alapvető Python könyvtárakat kell letölteni a virtuális környezetbe az implementáció első lépéseként?
Válasz: A virtuális környezetbe az implementáció első lépéseként a következő Python könyvtárakat kell letölteni: langchain, langchain-openai, langchain-community, chromadb, pydf, python-dotenv....

[Test 12/15] Kérdés: Milyen konkrét funkciót biztosít a jelenlegi projekt FastAPI endpointos megoldása?
Válasz: A jelenlegi projekt FastAPI endpointos megoldása tetszőleges PDF-ben való böngészésre ad lehetőséget....

[Test 13/15] Kérdés: Milyen típusú tokeneket/modellt használ az LLM rész az implementáció megvalósításához?
Válasz: A gpt 4.0 mini tokeneket használ az LLM rész megvalósításához....

[Test 14/15] Kérdés: Hogyan biztosítható, hogy a válaszok ne torzuljanak az egységgömbre vetítés közben?
Válasz: Nem található elegendő információ a dokumentumban....

[Test 15/15] Kérdés: Ki a szerzője és mi a címe a bibliográfiában szereplő 2020-as hivatkozásnak?
Válasz: A szerzője Tongzhou Wang és Phillip Isola, a címe "Understanding contrastive representation learning through alignment and uniformity on the hypersphere."...

Evaluáció kész! Sikeresen lekérdezve: 15/15 tesztkérdés.
```

## Installation & Setup

### 1. Clone the repository

git clone https://github.com/zenpeter-123/Genai-RAG-Assistant.git
cd Genai-RAG-Assistant

### 2. Create and activate a virtual environment

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up environment variables

Create a .env file in the root directory based on .env.example and add your OpenAI API key:

OPENAI_API_KEY=your-openai-api-key-here
EMBEDDING_MODEL=text-embedding-3-small
DEFAULT_MODEL=gpt-4o-mini
CHROMA_PERSIST_DIR=./chroma_db
PROJECT_NAME=Enterprise GenAI Document Assistant
API_V1_STR=/api/v1

## Running the Application

fastapi dev main.py

The API will be available at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/api/v1/openapi.json

## API Endpoints

### POST /api/v1/upload

Upload a PDF document for indexing.

curl -X POST "http://127.0.0.1:8000/api/v1/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@Markov chains.pdf;type=application/pdf"

Response:

{
  "filename": "Markov chains.pdf",
  "num_chunks": 76,
  "message": "Sikeresen indexelve 76 szövegblokk."
}

### POST /api/v1/chat

Ask a question based on the indexed documents.

curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "Mi a stacionárius eloszlás?", "top_k": 15}'

Response:

{
  "question": "Mi a stacionárius eloszlás?",
  "answer": "...",
  "sources": [
    {
      "page_content": "...",
      "page": 12,
      "source": "Markov chains.pdf"
    }
  ]
}

## Running Tests & Evaluation

### 1. Unit & Integration Tests (Pytest)

Run core application tests to verify endpoint stability:

pytest tests/ -v

Expected output:

10 passed in 27.30s

### 2. Automated RAG Evaluation

Run the automated evaluation script to test 15 domain-specific queries through the FastAPI test client:

python evaluate.py

Expected output:

=== RAG SYSTEM AUTOMATED EVALUATION ===
Dokumentum feltöltése és indexelése: project_documentation.pdf...
Sikeres feltöltés és indexelés!

[Test 1/15] Kérdés: Mi a RAG asszisztens alapvető célja a dokumentum szerint?
Válasz: A RAG asszisztens alapvető célja, hogy képes legyen a saját tudástárát ötvözve megadott dokumentumokat figyelembe véve választ adni a felhasználónak.

...

[Test 15/15] Kérdés: Ki a szerzője és mi a címe a bibliográfiában szereplő 2020-as hivatkozásnak?
Válasz: Nem található elegendő információ a dokumentumban.

Evaluáció kész! Sikeresen lekérdezve: 15/15 tesztkérdés.

## Technical Details

### Chunking

- Chunk size: 800 characters
- Chunk overlap: 150 characters

### Retrieval

- BM25: k=15 (keyword search)
- Vector: k=15 (semantic search)
- Ensemble: 50/50 weights
- Final: top 15 chunks

### LLM

- Model: gpt-4o-mini
- Temperature: 0
- Prompt: Hungarian, grounded on context only

## Future Improvements

- Add reranker (cross-encoder) for better precision
- Add Docker support
- Add CI/CD with GitHub Actions
- Add authentication for production
- Migrate to langchain-chroma (deprecation warning)
- Add streaming responses

## License

MIT

## Author

Patrik Madár

- GitHub: https://github.com/zenpeter-123
- Email: madarpatrik369@gmail.com
