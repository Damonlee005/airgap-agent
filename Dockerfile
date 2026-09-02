FROM python:3.12-slim

WORKDIR /app

# curl is just here for verify_isolation.sh, not used by the agent
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py conversation.py exceptions.py ollama_client.py agent.py ./
COPY utils/ ./utils/
COPY scripts/ ./scripts/

ENTRYPOINT ["python", "agent.py"]
