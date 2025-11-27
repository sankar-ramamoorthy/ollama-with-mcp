# backend/src/backend/tests/test_chat_mocked.py

import logging
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app import app

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use synchronous TestClient for simplicity
client = TestClient(app)


def test_chat_success_mocked():
    """
    Test /chat endpoint with a mocked successful response from Ollama service.
    """
    # This matches the internal key used by chat_reply()
    mocked_response = {"message": "Mocked LLM Response"}

    # Patch the chat_with_ollama function **where it is used**: in chat_service
    with patch("backend.services.chat_service.chat_with_ollama", return_value=mocked_response):
        logger.debug("Running test_chat_success_mocked")
        res = client.post("/chat", json={"message": "Hello"})
        assert res.status_code == 200
        assert res.json() == {"response": "Mocked LLM Response"}


def test_chat_error_from_ollama():
    """
    Test /chat endpoint when Ollama service raises an exception.
    The endpoint should handle the error gracefully and return fallback message.
    """
    # Patch to raise an exception
    with patch(
        "backend.services.chat_service.chat_with_ollama",
        side_effect=Exception("Ollama is down")
    ):
        logger.debug("Running test_chat_error_from_ollama")
        res = client.post("/chat", json={"message": "fail"})
        assert res.status_code == 200
        # Fallback message returned from chat_reply()
        assert res.json() == {"response": "No response from Ollama"}
