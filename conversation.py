class Conversation:
    # keeps the running message history for one session, trims old
    # messages once it gets long so it doesn't blow past the model's
    # context window

    def __init__(self, system_prompt=None, max_turns=20):
        self.max_turns = max_turns
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_user(self, content):
        self._add("user", content)

    def add_assistant(self, content):
        self._add("assistant", content)

    def _add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        system = [m for m in self.messages if m["role"] == "system"]
        rest = [m for m in self.messages if m["role"] != "system"]
        if len(rest) > self.max_turns * 2:
            rest = rest[-(self.max_turns * 2):]
        self.messages = system + rest

    def get_messages(self):
        return list(self.messages)

    def clear(self):
        system = [m for m in self.messages if m["role"] == "system"]
        self.messages = system
