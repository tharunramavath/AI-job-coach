import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_model() -> str:
    """Gets the active model from session state, falling back to environment variable or default."""
    if "groq_model" in st.session_state and st.session_state.groq_model:
        return st.session_state.groq_model
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def get_client() -> Groq:
    """Gets the Groq client, using session state API key or environment variable."""
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please enter it in the sidebar or in the .env file.")
    return Groq(api_key=api_key)


def chat(messages: list[dict], system: str = None, temperature: float = 0.7) -> str:
    """Single call to Groq LLaMA. Returns the assistant's text response."""
    client = get_client()
    model = get_model()

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

