import os

PDF_PATH = "Markov chains.pdf"


def test_rag_end_to_end(client):
    """Feltöltés → kérdés → releváns válasz a PDF-ből."""
    # 1. Feltöltés
    assert os.path.exists(PDF_PATH), f"A teszt PDF nem található: {PDF_PATH}"

    with open(PDF_PATH, "rb") as f:
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("Markov chains.pdf", f, "application/pdf")}
        )
    assert upload_response.status_code == 201

    # 2. Kérdés
    chat_response = client.post(
        "/api/v1/chat",
        json={"question": "Mi a stacionárius eloszlás?", "top_k": 30}
    )
    assert chat_response.status_code == 200

    # 3. Válasz ellenőrzése
    data = chat_response.json()
    answer = data["answer"]

    assert len(answer) > 50, "A válasz túl rövid"
    assert "nem található" not in answer.lower(), "A modell nem találta a választ"

    # 4. Források ellenőrzése
    sources = data["sources"]
    assert len(sources) > 0, "Nincsenek források"
    source_files = [s.get("source", "") for s in sources]
    assert any("Markov" in s for s in source_files), \
        "A források között nincs Markov chains.pdf"