# backend/src/backend/tests/test_chat.py

from fastapi.testclient import TestClient
from backend.app import app

import sys

client = TestClient(app)

def test_chat_endpoint():
    r = client.post("/chat", json={"message": "hi"})
    print("test chat sys.path",sys.path)
    assert r.status_code == 200
    # Expecting stub response from Ollama
    assert "Echo from Ollama" in r.json()["response"]
