# GenAI RAG Assistant

Enterprise-ready Retrieval-Augmented Generation (RAG) backend built with FastAPI, LangChain, ChromaDB, and OpenAI. Designed for modularity, clean code, and precise document-based question answering with source citations.

## Architecture & Theoretical Background

The system combines vector embeddings and large language models to answer user queries grounded in custom documents (e.g., PDF manuals, research papers).

- **Vector Space & Embeddings:** Documents and queries are mapped into a high-dimensional real vector space ($\mathbb{R}^{d}$, where $d = 1536$ for OpenAI embeddings) and projected onto a hyperspace unit sphere.
- **Distance Metric:** Semantic relevance is measured using cosine distance based on the angle between vectors:
  $$d(u, v) = \cos(\theta)$$
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
├── main.py                   # FastAPI application entry point with CORS middleware
├── rag_prototype.py          # CLI prototype script for local testing
├── requirements.txt          # Python dependencies
└── .env.example              # Environment variables template

Key Features
FastAPI Endpoints:

POST /api/v1/upload: Uploads and automatically parses/indexes PDF documents into the persistent ChromaDB vector store.

POST /api/v1/chat: Handles user queries through the RAG pipeline with configurable retrieval parameters.

Vector Search & Persistence: Powered by ChromaDB using LangChain wrappers and OpenAI embedding models.

Robust Anti-Hallucination Behavior: Built-in validation ensures safe fallbacks when context is missing.

Automated Evaluation: Includes an end-to-end testing script (evaluate.py) validating system accuracy across 15 domain-specific queries.

Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/zenpeter-123/Genai-RAG-Assistant.git](https://github.com/zenpeter-123/Genai-RAG-Assistant.git)
cd Genai-RAG-Assistant
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory based on .env.example and add your OpenAI API key:

Kódrészlet
OPENAI_API_KEY=your-openai-api-key-here
Running Tests & Evaluation
1. Unit & Integration Tests (Pytest)
Run core application tests to verify endpoint stability:

Bash
python -m pytest
2. Automated RAG Evaluation
Run the automated evaluation script to test 15 domain-specific queries through the FastAPI test client:

Bash
python evaluate.py
Automated Evaluation Results (15/15 Test Queries)
Plaintext
=== RAG SYSTEM AUTOMATED EVALUATION ===
Dokumentum feltöltése és indexelése: project_documentation.pdf...
Sikeres feltöltés és indexelés!

[Test 1/15] Kérdés: Mi a RAG asszisztens alapvető célja a dokumentum szerint?
Válasz: A RAG asszisztens alapvető célja, hogy képes legyen a saját tudástárát ötvözve megadott dokumentumokat figyelembe véve választ adni a felhasználónak.

[Test 2/15] Kérdés: Hány dimenziós valós vektorteret (d) használ az OpenAI modellje?
Válasz: Az OpenAI modellje egyd= 1536 dimenziós valós vektorteret használ.

[Test 3/15] Kérdés: Hova történik a pontok vetítése ebben a vektortér-konstrukcióban?
Válasz: A pontok vetítése az egységgömb felszínére történik ebben a vektortér-konstrukcióban.

[Test 4/15] Kérdés: Pontosan hogyan van definiálva az u és v vektorok közötti távolságmennyiség d(u,v)?
Válasz: Az u és v vektorok közötti távolságmennyiség d(u,v) a következőképpen van definiálva: d(u,v) = ⟨u;v⟩ = cos(θ), ahol θ az u és v vektorok közötti, origóból mért szög.

[Test 5/15] Kérdés: Mitől függ a skaláris szorzat értéke ebben a gömbi távolság-modellben?
Válasz: A skaláris szorzat értéke ebben a gömbi távolság-modellben csak a két vektor bezárt szögétől függ.

[Test 6/15] Kérdés: Mi a pontos célja az embedding modellnek a válaszok és kérdések egységgömbre vetítése mögött?
Válasz: Az embedding modell célja, hogy a válaszokat és kérdéseket úgy helyezze el a térben, hogy a relevanciát a távolságokkal tudja kifejezni, miközben az egymáshoz hasonló dolgokat közel húzza egymáshoz a gömbön, és közben megőrzi a többi választ is rajta, hogy ne történjen összehúzódás.

[Test 7/15] Kérdés: Melyik tudományos cikk foglalkozik a kontrasztív reprezentációtanulással a hiperszférán?
Válasz: A kontrasztív reprezentációtanulással a hiperszférán foglalkozó tudományos cikk a [WI20] hivatkozás alatt található: Tongzhou Wang és Phillip Isola. Understanding contrastive representation learning through alignment and uniformity on the hypersphere. CoRR, abs/2005.10242, 2020.

[Test 8/15] Kérdés: A kérdés gömbfelszíni vetületéhez viszonyítva hány legközelebb eső válasz vetületét határozzuk meg?
Válasz: Nem található elegendő információ a dokumentumban.

[Test 9/15] Kérdés: Hogyan osztja le a szerepeket a rendszer a ChromaDB és a nyelvi modell között?
Válasz: Nem található elegendő információ a dokumentumban.

[Test 10/15] Kérdés: Mi a RAG (Retrieval Augmentation Generation) folyamat pontos lépésről lépésre láncolata?
Válasz: A RAG (Retrieval Augmentation Generation) folyamat pontos lépésről lépésre láncolata a következő: 1. Embedding model, 2. ChromaDB, 3. LLM.

[Test 11/15] Kérdés: Mely alapvető Python könyvtárakat kell letölteni a virtuális környezetbe az implementáció első lépéseként?
Válasz: A virtuális környezetbe az implementáció első lépéseként a következő Python könyvtárakat kell letölteni: langchain, langchain-openai, langchain-community, chromadb, pypdf, python-dotenv.

[Test 12/15] Kérdés: Milyen konkrét funkciót biztosít a jelenlegi projekt FastAPI endpointos megoldása?
Válasz: A jelenlegi projekt FastAPI endpointos megoldása tetszőleges PDF-ben való böngészésre ad lehetőséget.

[Test 13/15] Kérdés: Milyen típusú tokeneket/modellt használ az LLM rész az implementáció megvalósításához?
Válasz: A gpt 4.0 mini tokeneket használ az LLM rész megvalósításához.

[Test 14/15] Kérdés: Hogyan biztosítható, hogy a válaszok ne torzuljanak az egységgömbre vetítés közben?
Válasz: Nem található elegendő információ a dokumentumban.

[Test 15/15] Kérdés: Ki a szerzője és mi a címe a bibliográfiában szereplő 2020-as hivatkozásnak?
Válasz: Nem található elegendő információ a dokumentumban.

Evaluáció kész! Sikeresen lekérdezve: 15/15 tesztkérdés.
