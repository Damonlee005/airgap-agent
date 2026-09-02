from unittest.mock import MagicMock, patch

import pytest
import requests

from exceptions import ModelResponseError, ModelUnreachableError
from ollama_client import OllamaClient


@pytest.fixture
def client():
    return OllamaClient(host="http://fake-ollama:11434", timeout=5)


def test_is_reachable_true(client):
    with patch("ollama_client.requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        assert client.is_reachable() is True


def test_is_reachable_false_on_connection_error(client):
    with patch("ollama_client.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        assert client.is_reachable() is False


def test_list_models_parses_names(client):
    with patch("ollama_client.requests.get") as mock_get:
        response = MagicMock()
        response.raise_for_status = lambda: None
        response.json.return_value = {"models": [{"name": "llama3"}, {"name": "mistral"}]}
        mock_get.return_value = response
        assert client.list_models() == ["llama3", "mistral"]


def test_list_models_raises_when_unreachable(client):
    with patch("ollama_client.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")
        with pytest.raises(ModelUnreachableError):
            client.list_models()


def test_chat_returns_content_for_requested_model(client):
    with patch("ollama_client.requests.post") as mock_post:
        response = MagicMock()
        response.raise_for_status = lambda: None
        response.json.return_value = {"message": {"content": "hello from llama3"}}
        mock_post.return_value = response
        result = client.chat("llama3", [{"role": "user", "content": "hi"}])
        assert result == "hello from llama3"
        sent_payload = mock_post.call_args.kwargs["json"]
        assert sent_payload["model"] == "llama3"


def test_chat_works_with_a_second_model(client):
    with patch("ollama_client.requests.post") as mock_post:
        response = MagicMock()
        response.raise_for_status = lambda: None
        response.json.return_value = {"message": {"content": "hello from mistral"}}
        mock_post.return_value = response
        result = client.chat("mistral", [{"role": "user", "content": "hi"}])
        assert result == "hello from mistral"
        sent_payload = mock_post.call_args.kwargs["json"]
        assert sent_payload["model"] == "mistral"


def test_chat_raises_on_empty_content(client):
    with patch("ollama_client.requests.post") as mock_post:
        response = MagicMock()
        response.raise_for_status = lambda: None
        response.json.return_value = {"message": {}}
        mock_post.return_value = response
        with pytest.raises(ModelResponseError):
            client.chat("llama3", [{"role": "user", "content": "hi"}])


def test_chat_retries_then_raises_unreachable(client):
    with patch("ollama_client.requests.post") as mock_post, \
         patch("time.sleep", return_value=None):
        mock_post.side_effect = requests.exceptions.ConnectionError("refused")
        with pytest.raises(ModelUnreachableError):
            client.chat("llama3", [{"role": "user", "content": "hi"}])
        assert mock_post.call_count == 3
