from conversation import Conversation


def test_starts_empty_without_system_prompt():
    convo = Conversation()
    assert convo.get_messages() == []


def test_system_prompt_is_first_message():
    convo = Conversation(system_prompt="be helpful")
    assert convo.get_messages() == [{"role": "system", "content": "be helpful"}]


def test_add_user_and_assistant():
    convo = Conversation()
    convo.add_user("hi")
    convo.add_assistant("hello")
    assert convo.get_messages() == [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
    ]


def test_trims_old_messages_but_keeps_system_prompt():
    convo = Conversation(system_prompt="be helpful", max_turns=2)
    for i in range(10):
        convo.add_user(f"message {i}")
        convo.add_assistant(f"reply {i}")

    messages = convo.get_messages()
    assert messages[0] == {"role": "system", "content": "be helpful"}
    assert len(messages) == 5
    assert messages[-1] == {"role": "assistant", "content": "reply 9"}


def test_clear_keeps_system_prompt_only():
    convo = Conversation(system_prompt="be helpful")
    convo.add_user("hi")
    convo.add_assistant("hello")
    convo.clear()
    assert convo.get_messages() == [{"role": "system", "content": "be helpful"}]


def test_clear_with_no_system_prompt_empties_fully():
    convo = Conversation()
    convo.add_user("hi")
    convo.clear()
    assert convo.get_messages() == []
