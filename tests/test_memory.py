from agent.memory import get_memory, clear_memory


def test_memory_created_for_new_user():
    memory = get_memory("user_001")
    assert memory is not None


def test_memory_isolated_between_users():
    memory_a = get_memory("user_a")
    memory_b = get_memory("user_b")
    memory_a.save_context({"input": "hello"}, {"output": "hi there"})
    history_b = memory_b.load_memory_variables({}).get("chat_history", [])
    assert len(history_b) == 0


def test_memory_persists_within_session():
    memory = get_memory("user_persist")
    memory.save_context({"input": "what is the pool hours?"}, {"output": "7am to 9pm"})
    history = memory.load_memory_variables({}).get("chat_history", [])
    assert len(history) > 0


def test_clear_memory():
    memory = get_memory("user_clear")
    memory.save_context({"input": "hello"}, {"output": "hi"})
    clear_memory("user_clear")
    fresh_memory = get_memory("user_clear")
    history = fresh_memory.load_memory_variables({}).get("chat_history", [])
    assert len(history) == 0


def test_clear_nonexistent_user():
    # Should not raise an error
    clear_memory("user_does_not_exist")
