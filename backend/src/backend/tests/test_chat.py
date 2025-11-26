from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_chat():
    r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 200
    assert r.json() == {"response": "This is a static response placeholder."}
