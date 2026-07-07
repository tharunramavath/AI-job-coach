import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def summarize_preferences(history: list[dict]) -> str:
    """Extracts key preferences mentioned by the user from conversation history."""
    if not history:
        return ""
    user_turns = [m["content"] for m in history if m["role"] == "user"]
    if not user_turns:
        return ""
    combined = "\n".join(f"- {t}" for t in user_turns[-10:])  # last 10 user messages
    return f"Previous things the user said:\n{combined}"


def chat(messages: list[dict], system: str = None, temperature: float = 0.7) -> str:
    """Helper to call Groq LLaMA directly."""
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please enter it in the sidebar.")
    model = st.session_state.get("groq_model") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    client = Groq(api_key=api_key)
    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    
    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def run_stage_5(history: list[dict]) -> str:
    """Generates a reply factoring in the in-session conversation history and preferences."""
    preferences_summary = summarize_preferences(history)
    
    system = f"""You are a job search coach with memory. You remember everything the user has told you and factor it into every response.

{preferences_summary}

When the user asks something, check if their past statements are relevant and incorporate them naturally — don't just repeat what they said, use it to give better advice."""

    return chat(messages=history, system=system)
