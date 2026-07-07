import streamlit as st
from ui.runner import render_stage_runner

st.set_page_config(page_title="Stage 2 — Memory & Context", layout="centered")
render_stage_runner(stage_num=2)
