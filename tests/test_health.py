def test_root_endpoint(client):
    """A root végpont visszaadja az üzenetet."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "running" in response.json()["message"].lower()


def test_docs_endpoint(client):
    """A /docs oldal betölt."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json(client):
    """Az OpenAPI JSON elérhető."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


    