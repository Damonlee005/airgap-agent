import logging

import requests

from config import OLLAMA_HOST, REQUEST_TIMEOUT
from exceptions import ModelResponseError, ModelUnreachableError
from utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)


class OllamaClient:
    # talks to ollama on the host. model gets passed in per call
    # instead of locked in at init, so one client can switch models
    # mid session without getting rebuilt

    def __init__(self, host=OLLAMA_HOST, timeout=REQUEST_TIMEOUT):
        self.host = host.rstrip("/")
        self.timeout = timeout

    def is_reachable(self):
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=self.timeout)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def list_models(self):
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=self.timeout)
            r.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise ModelUnreachableError(f"couldn't reach ollama at {self.host}: {exc}") from exc
        return [m["name"] for m in r.json().get("models", [])]

    @retry_with_backoff(retries=3, base_delay=1.0)
    def _post_chat(self, payload):
        return requests.post(f"{self.host}/api/chat", json=payload, timeout=self.timeout)

    def chat(self, model, messages):
        payload = {"model": model, "messages": messages, "stream": False}
        try:
            r = self._post_chat(payload)
            r.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise ModelUnreachableError(f"couldn't reach ollama at {self.host}: {exc}") from exc

        data = r.json()
        content = data.get("message", {}).get("content")
        if not content:
            raise ModelResponseError(f"unexpected response from ollama: {data}")
        return content.strip()
