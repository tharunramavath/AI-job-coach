import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def run_stage_1(user_input: str) -> str:
    """Direct LLM call without tools, memory, or context."""
    # 1. Get API Key and Model from Session State or Env
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please enter it in the sidebar.")
    model = st.session_state.get("groq_model") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # 2. Call Groq LLaMA
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a job search assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
