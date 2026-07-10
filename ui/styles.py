import os
import streamlit as st


def fetch_models(api_key: str) -> list[str]:
    if not api_key or len(api_key) < 10:
        return []
    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        models_resp = client.models.list()
        valid_models = [
            m.id
            for m in models_resp.data
            if "llama" in m.id or "mixtral" in m.id or "gemma" in m.id
        ]
        if not valid_models:
            valid_models = [m.id for m in models_resp.data]
        return sorted(valid_models)
    except Exception:
        return []


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

:root {
  --red:    #C8211A;
  --red2:   #A81A14;
  --cream:  #F5F0E8;
  --dark:   #1A1A1A;
  --mid:    #444444;
  --muted:  #777777;
  --border: #DDD5C8;
  --white:  #FFFFFF;
}

.stApp {
  background-color: var(--cream);
  font-family: 'Barlow', sans-serif;
  color: var(--dark);
}

header[data-testid="stHeader"] {
  background-color: rgba(0, 0, 0, 0) !important;
  background: transparent !important;
}

div[data-testid="stDecoration"] {
  background-image: none !important;
  background: transparent !important;
  display: none !important;
}


[data-testid="stSidebar"] {
  background-color: #EDE8DD;
  border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .st-emotion-cache-1cypcdb {
  color: var(--dark);
}

.block-container {
  padding-top: 1.5rem;
  padding-bottom: 2rem;
}

h1 {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: clamp(2rem, 6vw, 3.2rem);
  font-weight: 900;
  text-transform: uppercase;
  color: var(--dark);
  line-height: 1;
  letter-spacing: 0.01em;
  margin-bottom: 0.25rem;
}

h2 {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--dark);
  margin-bottom: 0.5rem;
  letter-spacing: 0.02em;
}

h3 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--dark);
}

p, li, .stMarkdown, .stText {
  font-family: 'Barlow', sans-serif;
  color: var(--mid);
  font-size: 0.92rem;
  line-height: 1.6;
}

.stage-label {
  display: inline-block;
  background: transparent;
  color: var(--red);
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding: 0;
  margin-bottom: 0.5rem;
  border: none;
}

.stage-label-duration {
  font-weight: 700;
  color: var(--muted);
  letter-spacing: 0.1em;
}

.response-box {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid var(--red);
  padding: 1rem 1.2rem;
  margin-top: 0.75rem;
  font-size: 0.9rem;
  color: var(--dark);
  line-height: 1.6;
  font-family: 'Barlow', sans-serif;
}

.thought-box {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid #4a6fa5;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--dark);
  font-family: 'Barlow', sans-serif;
}

.action-box {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid #d4790a;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--dark);
  font-family: 'Barlow', sans-serif;
}

.obs-box {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid #2e8b57;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--dark);
  font-family: 'Barlow', sans-serif;
}

.final-box {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid var(--red);
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--dark);
  font-family: 'Barlow', sans-serif;
}

.stButton > button {
  font-family: 'Barlow', sans-serif;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--white);
  background: var(--red);
  border: none;
  padding: 0.6rem 1.4rem;
  transition: background 0.15s;
  cursor: pointer;
}

.stButton > button:hover {
  background: var(--red2);
  border: none;
  color: var(--white);
}

.stButton > button:disabled {
  background: #ccc;
  color: #888;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  font-family: 'Barlow', sans-serif;
  background: var(--white);
  border: 1.5px solid var(--border);
  color: var(--dark);
  font-size: 0.9rem;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--red);
  box-shadow: 0 0 0 1px var(--red);
}

.stExpander {
  border: 1.5px solid var(--border);
  background: var(--white);
}

.stExpander details {
  font-family: 'Barlow', sans-serif;
  background: var(--white);
}

div[data-testid="stExpanderToggleIcon"] {
  color: var(--red);
}

.stAlert {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-left: 4px solid var(--red);
  color: var(--dark);
}

.stSuccess {
  background: #E8F5ED;
  border: 1px solid #9DCCAA;
  border-left: 4px solid #1E6B3A;
  color: #1E6B3A;
}

.stError {
  background: #FEF0EF;
  border: 1px solid var(--border);
  border-left: 4px solid var(--red);
  color: var(--red);
}

.stSpinner {
  color: var(--red);
}

.stCaption {
  font-family: 'Barlow', sans-serif;
  color: var(--muted);
  font-size: 0.8rem;
}

.stDivider {
  border-color: var(--border);
}

.stCode {
  background: var(--white);
  border: 1.5px solid var(--border);
  font-size: 0.82rem;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Custom Chat Bubbles for Stage 6 */
.chat-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 1rem;
  margin-bottom: 1rem;
  gap: 0.75rem;
}

.chat-bubble-user {
  background-color: #EDE8DD;
  color: #1A1A1A;
  padding: 0.8rem 1.2rem;
  border-radius: 15px 15px 0px 15px;
  max-width: 80%;
  align-self: flex-end;
  margin-left: auto;
  font-family: 'Barlow', sans-serif;
  border: 1px solid #DDD5C8;
  font-size: 0.95rem;
  line-height: 1.4;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.chat-bubble-agent {
  background-color: #FFFFFF;
  color: #1A1A1A;
  padding: 0.8rem 1.2rem;
  border-radius: 15px 15px 15px 0px;
  max-width: 80%;
  align-self: flex-start;
  margin-right: auto;
  font-family: 'Barlow', sans-serif;
  border: 1px solid #DDD5C8;
  border-left: 4px solid #C8211A;
  font-size: 0.95rem;
  line-height: 1.4;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.chat-bubble-agent p {
  margin: 0 0 0.5rem 0;
}
.chat-bubble-agent p:last-child {
  margin-bottom: 0;
}
</style>
"""


def apply_base_style():
    st.markdown(CSS, unsafe_allow_html=True)

    # Initialize session states
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

    if "groq_models_list" not in st.session_state:
        st.session_state.groq_models_list = []
        if st.session_state.groq_api_key:
            st.session_state.groq_models_list = fetch_models(
                st.session_state.groq_api_key
            )

    if "groq_model" not in st.session_state:
        st.session_state.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if "jina_api_key" not in st.session_state:
        st.session_state.jina_api_key = os.getenv("JINA_API_KEY", "")

    # API & Model sidebar controls
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 API & Model Settings")

    api_key_input = st.sidebar.text_input(
        "Groq API Key",
        value=st.session_state.groq_api_key,
        type="password",
        placeholder="gsk_...",
        help="Get your key from console.groq.com",
    )

    if api_key_input != st.session_state.groq_api_key:
        st.session_state.groq_api_key = api_key_input
        with st.sidebar.spinner("Fetching available models..."):
            st.session_state.groq_models_list = fetch_models(api_key_input)
            if st.session_state.groq_models_list:
                if "llama-3.3-70b-versatile" in st.session_state.groq_models_list:
                    st.session_state.groq_model = "llama-3.3-70b-versatile"
                else:
                    st.session_state.groq_model = st.session_state.groq_models_list[0]
            else:
                st.session_state.groq_model = ""
        st.rerun()

    if st.session_state.groq_models_list:
        try:
            default_index = st.session_state.groq_models_list.index(
                st.session_state.groq_model
            )
        except ValueError:
            default_index = 0

        selected_model = st.sidebar.selectbox(
            "Select Model",
            options=st.session_state.groq_models_list,
            index=default_index,
        )
        st.session_state.groq_model = selected_model
    else:
        if st.session_state.groq_api_key:
            st.sidebar.warning("Failed to fetch models. Check key.")
        else:
            st.sidebar.info("Enter Groq API Key to populate models.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Jina Search API")

    jina_key_input = st.sidebar.text_input(
        "Jina API Key",
        value=st.session_state.jina_api_key,
        type="password",
        placeholder="jina_...",
        help="Get your free key from jina.ai (no credit card needed)",
    )

    if jina_key_input != st.session_state.jina_api_key:
        st.session_state.jina_api_key = jina_key_input
        st.rerun()


def stage_header(stage_num: int, title: str, duration: str, concept: str):
    st.markdown(
        f'<div class="stage-label">'
        f"LEVEL {stage_num:02d} "
        f'<span class="stage-label-duration">| {duration}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h1 style="margin-top:0">{title}</h1>',
        unsafe_allow_html=True,
    )
    st.caption(concept)
    st.divider()


def response_box(text: str):
    st.markdown(f'<div class="response-box">{text}</div>', unsafe_allow_html=True)
