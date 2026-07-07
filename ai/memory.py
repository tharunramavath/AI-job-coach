"""
In-session conversation memory.
Stored as a Python list in st.session_state — no disk, no DB.
"""


def init_memory(session_state, key: str = "chat_history"):
    if key not in session_state:
        session_state[key] = []


def add_message(session_state, role: str, content: str, key: str = "chat_history"):
    session_state[key].append({"role": role, "content": content})


def get_history(session_state, key: str = "chat_history") -> list[dict]:
    return session_state.get(key, [])


def clear_memory(session_state, key: str = "chat_history"):
    session_state[key] = []


def summarize_preferences(history: list[dict]) -> str:
    """
    Extracts key preferences mentioned by the user from conversation history.
    Returns a plain-text summary to inject into system prompt.
    """
    if not history:
        return ""
    user_turns = [m["content"] for m in history if m["role"] == "user"]
    if not user_turns:
        return ""
    combined = "\n".join(f"- {t}" for t in user_turns[-10:])  # last 10 user messages
    return f"Previous things the user said:\n{combined}"
