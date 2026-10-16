import os

PDF_PATH = "Markov chains.pdf"


def test_upload_valid_pdf(client):
    """Érvényes PDF feltöltése 201-es státuszkódot ad."""
    assert os.path.exists(PDF_PATH), f"A teszt PDF nem található: {PDF_PATH}"

    with open(PDF_PATH, "rb") as f:
        response = client.post(
            "/api/v1/upload",
            files={"file": ("Markov chains.pdf", f, "application/pdf")}
        )

    assert response.status_code == 201
    data = response.json()
    assert "filename" in data
    assert "num_chunks" in data
    assert data["num_chunks"] > 0


def test_upload_invalid_file_type(client):
    """Nem PDF fájl feltöltése 400-as hibát ad."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", b"not a pdf", "text/plain")}
    )
    assert response.status_code == 400


def test_upload_no_file(client):
    """Fájl nélküli feltöltés 422-es validációs hibát ad."""
    response = client.post("/api/v1/upload")
    assert response.status_code == 422