import streamlit as st
from ui.runner import render_stage_runner

st.set_page_config(page_title="Stage 3 — LLM + Tools", layout="centered")
render_stage_runner(stage_num=3)
