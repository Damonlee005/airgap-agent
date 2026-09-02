import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# models I've actually pulled and tested against, not exhaustive
SUPPORTED_MODELS = ["llama3", "mistral", "phi3", "gemma2"]
