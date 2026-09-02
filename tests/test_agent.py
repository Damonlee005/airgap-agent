from unittest.mock import MagicMock

from agent import resolve_model
from exceptions import ModelUnreachableError


def test_resolve_model_returns_requested_when_available():
    client = MagicMock()
    client.list_models.return_value = ["llama3", "mistral"]
    assert resolve_model(client, "mistral") == "mistral"


def test_resolve_model_falls_back_when_not_pulled():
    client = MagicMock()
    client.list_models.return_value = ["llama3", "mistral"]
    result = resolve_model(client, "phi3")
    assert result == "llama3"


def test_resolve_model_switching_between_two_models():
    client = MagicMock()
    client.list_models.return_value = ["llama3", "mistral"]

    first = resolve_model(client, "llama3")
    second = resolve_model(client, "mistral")

    assert first == "llama3"
    assert second == "mistral"
    assert first != second


def test_resolve_model_uses_requested_when_host_unreachable():
    client = MagicMock()
    client.list_models.side_effect = ModelUnreachableError("down")
    result = resolve_model(client, "llama3")
    assert result == "llama3"
