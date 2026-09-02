class AgentError(Exception):
    pass


class ModelUnreachableError(AgentError):
    # ollama isn't running, or the container can't reach it
    pass


class ModelResponseError(AgentError):
    # got a response back but it wasn't usable
    pass
