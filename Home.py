import streamlit as st
from ui.styles import apply_base_style

st.set_page_config(
    page_title="AI Job Agent — Workshop", page_icon="🤖", layout="centered"
)
apply_base_style()

st.markdown(
    """
    <style>
    /* Global styling overrides */
    .stApp {
        background-color: #F5F0E8 !important;
    }
    
    .main-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: clamp(3rem, 8vw, 4.8rem);
        font-weight: 900;
        line-height: 0.9;
        text-transform: uppercase;
        color: #1A1A1A;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    .main-subtitle {
        font-family: 'Barlow', sans-serif;
        font-size: clamp(1rem, 2.5vw, 1.15rem);
        color: #777777;
        margin-bottom: 3rem;
    }

    /* Flexbox stage row to align button and card heights */
    .stage-row {
        display: flex;
        align-items: stretch;
        margin-bottom: 1.5rem;
        width: 100%;
        gap: 1.5rem;
    }

    /* Left Card styling */
    .stage-card {
        flex: 1;
        background-color: #FFFFFF;
        border: 1px solid #DDD5C8;
        border-left: 4px solid #C8211A;
        padding: 1.5rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .stage-num {
        font-family: 'Barlow Condensed', sans-serif;
        color: #C8211A;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
    }

    .stage-title {
        font-family: 'Barlow Condensed', sans-serif;
        color: #1A1A1A;
        font-size: clamp(1.4rem, 3.5vw, 1.8rem);
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .stage-desc {
        font-family: 'Barlow', sans-serif;
        color: #555555;
        font-size: 0.95rem;
        line-height: 1.4;
    }

    /* Arrow button styling */
    .stage-arrow-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        min-width: 60px;
        border: 1.5px solid #C8211A;
        background-color: transparent;
        color: #C8211A !important;
        font-size: 1.6rem;
        font-weight: bold;
        text-decoration: none !important;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }

    .stage-arrow-btn:hover {
        background-color: #C8211A;
        color: #FFFFFF !important;
    }
    </style>
    
    <div class="main-title">BUILD YOUR FIRST<br>AI AGENT</div>
    <div class="main-subtitle">6 stages. Same use case. One architecture evolution.</div>
    
    <!-- Stage 01 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 01</div>
        <div class="stage-title">NAIVE LLM</div>
        <div class="stage-desc">Direct LLM call without tools, memory, or context.</div>
      </div>
      <a href="./Stage_1_Naive_LLM" target="_self" class="stage-arrow-btn">→</a>
    </div>

    <!-- Stage 02 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 02</div>
        <div class="stage-title">CONTEXT & MEMORY</div>
        <div class="stage-desc">Resume context injected into the system prompt.</div>
      </div>
      <a href="./Stage_2_Memory_and_Context" target="_self" class="stage-arrow-btn">→</a>
    </div>

    <!-- Stage 03 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 03</div>
        <div class="stage-title">LLM + TOOLS</div>
        <div class="stage-desc">Real-time job search tool integration via Jina API.</div>
      </div>
      <a href="./Stage_3_LLM_and_Tools" target="_self" class="stage-arrow-btn">→</a>
    </div>

    <!-- Stage 04 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 04</div>
        <div class="stage-title">REACT AGENT</div>
        <div class="stage-desc">Thought → Action → Observation autonomous loop.</div>
      </div>
      <a href="./Stage_4_ReAct_Agent" target="_self" class="stage-arrow-btn">→</a>
    </div>

    <!-- Stage 05 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 05</div>
        <div class="stage-title">PERSISTENT MEMORY</div>
        <div class="stage-desc">Active conversation memory across multi-turn messages.</div>
      </div>
      <a href="./Stage_5_Persistent_Memory" target="_self" class="stage-arrow-btn">→</a>
    </div>

    <!-- Stage 06 -->
    <div class="stage-row">
      <div class="stage-card">
        <div class="stage-num">STAGE 06</div>
        <div class="stage-title">FULL AGENT</div>
        <div class="stage-desc">LangGraph-inspired wiring of memory, reasoning, and tools.</div>
      </div>
      <a href="./Stage_6_The_Full_Agent" target="_self" class="stage-arrow-btn">→</a>
    </div>
    """,
    unsafe_allow_html=True,
)
