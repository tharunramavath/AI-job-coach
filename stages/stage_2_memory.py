import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


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


def run_stage_2(user_input: str, resume: str) -> dict:
    """Runs both the naive (dumb) response and context-aware response for contrast."""
    dumb_response = chat(
        messages=[{"role": "user", "content": user_input}],
        system="You are a job search assistant.",
    )
    
    system = f"""You are a job search assistant. Use the user's background below to give specific, relevant advice.

User background:
{resume}"""
    
    context_response = chat(
        messages=[{"role": "user", "content": user_input}],
        system=system,
    )
    
    return {
        "without_context": dumb_response,
        "with_context": context_response
    }
