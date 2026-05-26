from langchain.memory import ConversationBufferMemory

# Store memory per user session
_memory_store: dict[str, ConversationBufferMemory] = {}


def get_memory(user_id: str) -> ConversationBufferMemory:
    if user_id not in _memory_store:
        _memory_store[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
    return _memory_store[user_id]


def clear_memory(user_id: str) -> None:
    if user_id in _memory_store:
        del _memory_store[user_id]
