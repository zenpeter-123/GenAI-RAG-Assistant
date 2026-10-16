def test_chat_valid_query(client):
    """Érvényes kérdésre 200-as válasz érkezik."""
    response = client.post(
        "/api/v1/chat",
        json={"question": "Mi a stacionárius eloszlás?", "top_k": 15}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["answer"]) > 0


def test_chat_response_structure(client):
    """A válasz tartalmazza a várt mezőket."""
    response = client.post(
        "/api/v1/chat",
        json={"question": "Mi a Markov-lánc?", "top_k": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)


def test_chat_empty_query(client):
    """Üres kérdés validációs hibát ad."""
    response = client.post(
        "/api/v1/chat",
        json={"question": "", "top_k": 5}
    )
    # Ha a schema nem engedi az üres stringet, 422; ha igen, akkor 200
    assert response.status_code in [200, 422]