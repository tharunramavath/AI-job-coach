# AI Job Agent — Gradientts Workshop

Build a reasoning AI job coach from scratch in 90 minutes.

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys
cp .env.example .env
# Edit .env and add:
#   GROQ_API_KEY=...    → https://console.groq.com
#   JINA_API_KEY=...    → https://jina.ai (free tier, no credit card)

# 3. Run
streamlit run Home.py
```

## Project Structure

```
job_agent_workshop/
│
├── Home.py                        # Landing page
│
├── pages/
│   ├── 1_Stage_1_Dumb_Oracle.py  # Just an LLM, no context
│   ├── 2_Stage_2_Memory.py       # Resume as system prompt context
│   ├── 3_Stage_3_Tools.py        # Real job search via Jina API
│   ├── 4_Stage_4_ReAct.py        # Thought → Action → Observation loop
│   ├── 5_Stage_5_Persistent_Memory.py  # In-session conversation memory
│   └── 6_Stage_6_Full_Agent.py   # Everything wired together
│
├── ai/
│   ├── llm.py      # Groq LLaMA 3.1 70B client
│   ├── tools.py    # Jina Search API (real job listings)
│   ├── react.py    # ReAct loop logic
│   └── memory.py   # In-session memory helpers
│
└── ui/
    └── styles.py   # Minimal white UI, shared across all pages
```

## Teaching flow

Each page = one stage. During the live class:
- Show only the relevant page
- The AI logic lives in `ai/` — explain that in the terminal/editor
- The UI is intentionally minimal — your PPT carries the visual story

## API Keys

| Key | Where to get | Cost |
|-----|-------------|------|
| `GROQ_API_KEY` | console.groq.com | Free tier available |
| `JINA_API_KEY` | jina.ai | Free — 1M tokens/month, no credit card |
