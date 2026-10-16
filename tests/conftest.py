import pytest
from fastapi.testclient import TestClient
from main import app
import os
from app.services.rag_service import rag_service


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient a tesztekhez."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def upload_pdf_before_each_test(client):

    """Minden teszt előtt törli a ChromaDB-t, és újra feltölti a PDF-et."""
    # ChromaDB törlése
    try:
        rag_service.vectorstore.delete_collection()
        rag_service.vectorstore = rag_service.vectorstore.__class__(
            collection_name="enterprise_pdf_rag",
            embedding_function=rag_service.embeddings,
            persist_directory=rag_service.persist_directory
        )
    except Exception:
        pass


    import os
    pdf_path = "Markov chains.pdf"
    if not os.path.exists(pdf_path):
        pytest.skip(f"A teszt PDF nem található: {pdf_path}")

    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/v1/upload",
            files={"file": ("Markov chains.pdf", f, "application/pdf")}
        )
    assert response.status_code == 201, "A PDF feltöltése sikertelen"