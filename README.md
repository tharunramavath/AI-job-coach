# AI Job Agent

Build a reasoning AI job coach that evolves from a basic LLM call into a full agent with real-time job search, skills gap analysis, and conversation memory.

## Features

- **6 stages** — Each page shows the agent at a different level of capability: naive LLM → resume context → tool use → ReAct loop → persistent memory → full pipeline agent
- **Real-time job search** — Searches live job listings via the Jina Reader API
- **Skills gap analysis** — Locally compares your resume against job descriptions (no LLM needed)
- **Conversation memory** — Remembers preferences across multi-turn chats

## Prerequisites

- Python 3.10+
- A [Groq](https://console.groq.com) API key (free tier)
- A [Jina](https://jina.ai) API key (free tier, no credit card)

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys
cp .env.example .env
# Edit .env and add your keys:
#   GROQ_API_KEY=gsk_...
#   JINA_API_KEY=jina_...

# 3. Launch the app
streamlit run Home.py
```

You can also enter your Groq API key directly in the app's sidebar — it will fetch available models automatically.

## Project Structure

```
├── Home.py                        # Landing page with stage navigation
├── pages/                         # Streamlit multi-page app files
│   ├── 1_Stage_1_Naive_LLM.py
│   ├── 2_Stage_2_Memory_and_Context.py
│   ├── 3_Stage_3_LLM_and_Tools.py
│   ├── 4_Stage_4_ReAct_Agent.py
│   ├── 5_Stage_5_Persistent_Memory.py
│   └── 6_Stage_6_The_Full_Agent.py
├── stages/                        # Core stage logic (imported by pages)
│   ├── stage_1_oracle.py
│   ├── stage_2_memory.py
│   ├── stage_3_tools.py
│   ├── stage_4_react.py
│   ├── stage_5_persistent_memory.py
│   └── stage_6_full_agent.py
├── ai/                            # AI modules
│   ├── llm.py                     # Groq LLaMA client
│   ├── tools.py                   # Jina search + skills gap analyzer
│   ├── react.py                   # ReAct loop logic
│   └── memory.py                  # Session memory helpers
├── ui/                            # UI components
│   ├── styles.py                  # Global styling, sidebar controls
│   └── runner.py                  # Stage renderer (wires stages to pages)
└── requirements.txt
```

## API Keys

| Key | Where to get | Cost |
|-----|-------------|------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | Free tier available |
| `JINA_API_KEY` | [jina.ai](https://jina.ai) | Free — 1M tokens/month, no credit card |
