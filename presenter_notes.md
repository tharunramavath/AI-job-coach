# AI Job Agent Workshop — Presenter Guide & Speaker Notes

This guide is designed to help you run the webinar seamlessly. Each stage corresponds to a file under the `stages/` folder. Use these structured scripts, code explanations, sample inputs, and anticipated student Q&As to lead the session.

---

## 🛠️ Pre-Session Setup Checklist
Before starting the live broadcast, make sure:
1. Streamlit is running: `streamlit run Home.py`
2. Groq and Jina API keys are saved in your `.env` file or you have them ready to paste into the sidebar.
3. You have `stages/` and `pages/` open in your code editor side-by-side.

---

## 🏁 Stage 01: Naive LLM (The Dumb Oracle)
**File**: `stages/stage_1_oracle.py`

### 🏗️ Architecture
```
User Query ──► [ Groq LLM (Parametric Weights Only) ] ──► Response
```

### 🗣️ What to Say (Speaker Script)
> *"Welcome, everyone! Today, we are building a reasoning AI Job Agent from scratch. Let's start with Stage 1: The Dumb Oracle. At this level, we are doing a direct, raw LLM call. There is no memory, no tools, and no custom background. Think of this as the basic ChatGPT template. Let's ask it a career question and look at the response."*

### 📝 Code Explanation
* **`st.session_state.get("groq_api_key")`**: Dynamically checks if the user provided an API key in the sidebar, falling back to the environment variable.
* **`client.chat.completions.create(...)`**: Sends a single-turn payload directly to Groq.
* **`system: "You are a job search assistant."`**: A generic system instruction with no specific user background context.

### 📥 Sample Inputs & Demo
* **Sample Input 1**: `"What jobs should I apply for?"`
  * *Explanation*: The Dumb Oracle turns around and responds with a questionnaire asking for your degree, experience level, location, and salary goals because it has absolutely zero context about your background.
* **Sample Input 2**: `"Review my skills and recommend roles."`
  * *Explanation*: The LLM states it cannot see or inspect your profile, requesting you to paste your resume/background text so it has something to reference.



### ❓ Anticipated Student Doubts & Answers
* **Q: Why does the LLM give such generic responses?**
  * **A**: Because LLMs have no context about you. An LLM cannot give specific advice without knowing your degree, skills, location, or experience.
* **Q: Why are we using Groq?**
  * **A**: Groq offers ultra-low latency inference, which makes live agents feel fast and responsive (outputs in milliseconds rather than seconds).

---

## 🧠 Stage 02: Context & Memory (Give It a Brain)
**File**: `stages/stage_2_memory.py`

### 🏗️ Architecture
```
User Query ──┐
             ├─► [ Groq LLM ] ──► Response
Resume Text ─┘ (System Prompt Context)
```

### 🗣️ What to Say (Speaker Script)
> *"Now let's look at Stage 2. We're going to inject a 'brain' into our chatbot by feeding it a resume. In our code, we take the user's resume and dynamically write it directly into the System Prompt. Let's compare Stage 1's generic output to Stage 2's personalized output side-by-side using the same question."*

### 📝 Code Explanation
* **Inlined `chat()` helper**: Standardized function to handle dynamic API key/model routing.
* **`system = f"User background: {resume}"`**: Injects the raw resume context inside the system instruction. This forms the agent's short-term/in-context memory.
* **Double Call**: Executes one naive query and one context-aware query to illustrate the contrast.

### 📥 Sample Inputs & Demo
* **Sample Input 1**: `"What jobs should I apply for?"` (Using default resume: Priya Sharma, B.Tech CS 2024, Python, ML, VIT Vellore)
  * *Explanation*: The context-aware completion immediately recommends entry-level ML Engineer, Python developer, or Junior Data Analyst roles in India, matching VIT Vellore and the ML projects listed in the resume.
* **Sample Input 2**: `"Am I qualified to apply for a senior Engineering Manager position?"`
  * *Explanation*: The LLM reads the resume, notices you are a 2024 fresher graduate with no leadership experience, and politely recommends targeting entry-level contributor tracks instead.



### ❓ Anticipated Student Doubts & Answers
* **Q: Is this real memory?**
  * **A**: No, this is "in-context" memory. It's stored in the prompt window (system instructions) for this single completion. If you reload the session, it forgets everything unless we pass the resume again.
* **Q: What happens if the resume is extremely long?**
  * **A**: It eats up your token budget (context window). For larger resumes, we would implement RAG (Retrieval-Augmented Generation) to extract only relevant sections.

---

## 👁️ Stage 03: LLM + Tools (Give It Eyes & Analytics)
**File**: `stages/stage_3_tools.py`

### 🏗️ Architecture
```
User Query ──► [ Jina Search API ] ──► List of Jobs 
                                           │
                                           ▼
                                 [ Skills Gap Analyzer ] ──┐
                                                           ├─► [ Groq LLM ] ──► Response
User Background ───────────────────────────────────────────┘
```

### 🗣️ What to Say (Speaker Script)
> *"Our agent now has a brain, but it's blind. It only knows what was in its training data. In Stage 3, we give our agent 'eyes' by introducing a tool: the Jina Search API. We will run a real-time web search for active job listings. But we don't stop there! We also run a local 'Skills Gap Analyzer' tool that compares the user's background text against each job description. This lets us calculate a match score (0-100%) and pinpoint missing skills for each job listing automatically, before the LLM synthesizes the advice!"*

### 📝 Code Explanation
* **`search_jobs(query)`**: Sends a requests GET call to `https://s.jina.ai/` searching LinkedIn, Naukri, and Indeed. Jina translates the resulting HTML pages into clean text format.
* **`analyze_skills_gap(background, job_description)`**: Intersects the user's background text against the job description using a local key list (`COMMON_SKILLS`), determining a match score, matching skills, and missing skills.
* **`format_jobs(jobs, resume_snippet)`**: Combines Jina's search output with the skills gap analysis, rendering match metrics directly in the tool output console.
* **Synthesizer Call**: Passes the detailed match metrics into the LLM as user context, asking it to match them against the user's profile and recommend application strategies.

### 📥 Sample Inputs & Demo
* **Sample Input 1**: `"ML Engineer jobs in Bangalore"` (Background snippet: `"B.Tech CS 2024, Python, ML, TensorFlow"`)
  * *Explanation*: Jina retrieves actual LinkedIn/Naukri job listings. The local Skills Gap tool evaluates matching scores (e.g. 75% match, highlighting missing skills like PyTorch), and the LLM suggests listings.
* **Sample Input 2**: `"Frontend developer openings"` (Background snippet: `"B.Tech CS 2024, Python, ML, TensorFlow"`)
  * *Explanation*: Jina searches for frontend postings. The local parser calculates a match score of 0% (missing HTML, CSS, React, JS), and the LLM warns the user that their Python/ML background does not align with these roles.

### ❓ Anticipated Audience Doubts & Answers
* **Q: Why use Jina Reader API instead of Google Search or BeautifulSoup?**
  * **A**: Normal search APIs return raw HTML which is bloated and wastes LLM tokens. Jina Reader searches the web and returns clean, LLM-optimized Markdown/text directly.
* **Q: Is the Skills Gap Analyzer calling an LLM?**
  * **A**: No! It runs purely in local Python code. This shows that tools can be simple, deterministic scripts (saving speed and API costs) rather than calling the LLM for everything.
* **Q: Can the LLM click the links?**
  * **A**: No. The LLM only sees the text snippets we fetch for it. The links are rendered for the human user to click.

---

## ⚖️ Stage 04: ReAct Agent (Give It Judgment)
**File**: `stages/stage_4_react.py`


### 🏗️ Architecture
```
                      ┌──────────────────────┐
                      ▼                      │ (New Observation)
User Query ──► [ Groq LLM ] ──► Action? ──► [ Jina Search ] 
                      │ (No: Final Answer)
                      ▼
                   Response
```

### 🗣️ What to Say (Speaker Script)
> *"In Stage 3, we forced the agent to search the web every single time. But a real agent needs judgment. It should decide when to search the web and when to answer from memory. In Stage 4, we build a ReAct (Reason + Act) loop. We prompt the LLM to write its thoughts, call tools using a specific syntax, read the observations, and loop until it has the final answer."*

### 📝 Code Explanation
* **`REACT_SYSTEM` Prompt**: Instructs the LLM to respond in the format `Thought: ...` and `Action: search_jobs(...)` or `Final Answer: ...`.
* **The Loop (`for _ in range(max_iterations):`)**:
  1. Call LLM with current messages.
  2. Parse response using Regex: check for `Action:` or `Final Answer:`.
  3. If `Action:` is found, execute `search_jobs(query)`, append the result as an `Observation:`, and run the loop again.
  4. If `Final Answer:` is found, break and output the response.

### 📥 Sample Inputs & Demo
* **Sample Input 1 (Factual/No Search)**: `"Can you explain what a Machine Learning Engineer does?"`
  * *Explanation*: The agent classifies this as a conceptual question. Its reasoning trace shows: `Thought` ──► decides no tool execution is required ──► immediately outputs `Final Answer` in a single completion step.
* **Sample Input 2 (Active Search)**: `"Find me ML jobs in Hyderabad"`
  * *Explanation*: The agent identifies the need for real-time listings. Reasoning trace: `Thought` ──► emits `Action: search_jobs("ML Engineer jobs in Hyderabad")` ──► execution receives Jina listings ──► `Thought` (evaluates listings) ──► compiles matches in `Final Answer`.
* **Sample Input 3 (Profile Factual/No Search)**: `"What skills does a software engineer need?"`
  * *Explanation*: The agent answers directly from parametric weights using internal reasoning, skipping search tool invocations.


### ❓ Anticipated Student Doubts & Answers
* **Q: What happens if the LLM gets stuck in an infinite loop?**
  * **A**: We hardcode `max_iterations = 4` to prevent infinite loops and runaway API costs.
* **Q: How do we prevent the agent from executing the exact same search query repeatedly?**
  * **A**: We implement two layers of defense: First, we add a rule in the `REACT_SYSTEM` prompt forbidding duplicate queries. Second, we code a guardrail in the loop using an `executed_queries` set tracker. If a duplicate query is intercepted, we inject a correction prompt as an observation, forcing the agent to vary its keywords or synthesize its final answer.
* **Q: Why do we use Regex instead of JSON mode?**
  * **A**: Regex on standard text formatting is lightweight and easier for students to parse during a live walkthrough. In production, structured JSON outputs (e.g., OpenAI function calling or LangChain/LangGraph) are preferred.

---

## 🔄 Stage 05: Persistent Memory (Give It Continuity)
**File**: `stages/stage_5_persistent_memory.py`

### 🏗️ Architecture
```
User Query ─────────┐
                    ├─► [ Groq LLM ] ──► Response
Session History ────┘ (st.session_state)
```

### 🗣️ What to Say (Speaker Script)
> *"Right now, every time we talk to our agent, it's a blank slate. In Stage 5, we add conversation memory. We will maintain a running list of chat messages, analyze user statements to summarize their career preferences, and inject that preference summary into the system prompt of every turn."*

### 📝 Code Explanation
* **`summarize_preferences(history)`**: Iterates over the last 10 user messages and builds a clean bulleted list of statements.
* **System Prompt compilation**: Merges the preference summary dynamically into the system message.
* **State Management**: Appends user inputs and assistant responses to a list stored inside Streamlit's `st.session_state`.

### 📥 Sample Inputs & Demo
* **Turn 1 (Preference setting)**: `"I prefer remote-first startups and working with Python."`
  * *Explanation*: The agent processes this statement and confirms it has saved these preferences. In the background, `summarize_preferences` extracts this into the system prompt context.
* **Turn 2 (Preference evaluation)**: `"Suggest some companies I should check out."`
  * *Explanation*: The agent retrieves your preferences from the summarized context and recommends Python-heavy remote companies (such as GitLab, Automattic, or HashiCorp).
* **Turn 3 (Adding preferences)**: `"Also, I want to avoid web development roles."`
  * *Explanation*: The agent appends this to the preference summary list. If you ask for job ideas next, it will suggest data science/ML positions instead of django web developer roles.


### ❓ Anticipated Student Doubts & Answers
* **Q: Where is this memory stored?**
  * **A**: In `st.session_state` (in-memory). If the user refreshes the browser, it is cleared. In production, you would back this up to a database (like PostgreSQL, DynamoDB, or Redis).
* **Q: Why don't we just pass the entire chat history instead of summarizing preferences?**
  * **A**: We do pass the chat history (`llm_messages = [m for m in history]`) so the LLM remembers the immediate context. However, extracting key preferences explicitly into the system prompt ensures the LLM highlights and enforces those rules consistently.

---

## 🤖 Stage 06: The Full Agent (All Wired Together)
**File**: `stages/stage_6_full_agent.py`

### 🏗️ Architecture
```
User Query ──► [ Router Heuristic ] ──► Trigger Search?
                       │                      │ (Yes)
                       │                      ▼
                       │               [ Jina Search ] ──► [ Skills Gap Analyzer ]
                       │                                            │
                       ▼                                            ▼
           [ Compile Prompt: Resume + Chat History + Tool Results ] ──► [ Groq LLM ] ──► Response
```

### 🗣️ What to Say (Speaker Script)
> *"We've reached the final stage. We are wiring everything together: short-term resume memory (Stage 2), real-time Jina search tools (Stage 3), and multi-turn conversational memory (Stage 5). This architecture represents the foundation of production AI agents. Let's see it in action as a complete career coach."*

### 📝 Code Explanation
* **`should_search(user_input)`**: A keyword heuristic classifier that determines whether the user's latest query requires executing a live job search.
* **Unified Pipeline**:
  1. Receives input -> Classifies if search is needed.
  2. If yes, queries Jina API, formats results, and appends to the tool context.
  3. Builds a master system prompt combining the parsed resume + conversation preferences + tool context.
  4. Submits the active chat log to Groq LLaMA to generate the final response.

### 📥 Sample Inputs & Demo
* **Setup**: Paste Priya Sharma's default resume in the container.
* **Turn 1 (Active Search with specific job links)**: `"Find me entry-level ML engineer jobs in Bangalore."`
  * *Explanation*: The routing logic classifies this as a search query. Jina Search triggers (filtering for specific postings), runs the Skills Gap Analyzer, and outputs job links with Match Scores (e.g. 75%) in the console. The agent streams matching advice.
* **Turn 2 (Memory turn matching to resume details)**: `"Which of those matches my TensorFlow background best?"`
  * *Explanation*: The routing logic bypasses the search tool because no new listings are requested. The LLM references the search history and Priya's resume TensorFlow project to highlight the specific Bangalore ML engineer listing.
* **Turn 3 (Concept/Preparation turn)**: `"How should I prepare for the interview for that specific position?"`
  * *Explanation*: The router again bypasses Jina search. The agent streams interview preparation topics customized specifically to the job description requirements and the user's resume background.


### ❓ Anticipated Audience Doubts & Answers
* **Q: By definition, an agent understands a goal and executes a task. Stage 6 looks like a chatbot — what makes it an Agent?**
  * **A**: Chat is just the **delivery mechanism (UI/UX)**, not the architecture. A chatbot answers questions using static parametric weights (e.g. Stage 1/2). Stage 6 is a **Routing/Pipeline Agent** because it accepts a high-level goal, programmatically decides if it needs to query the outside world (decision/classification), runs external tools (Jina Job Search and Skills Gap Matcher), and uses memory (resume context and session state) to fulfill the task.
* **Q: What is the main difference between Stage 4 (ReAct) and Stage 6?**
  * **A**: 
    - **Stage 4 (Autonomous ReAct)**: Uses the LLM in a loop to think, execute tools, observe, and decide when to stop. High autonomy, but high latency (multiple LLM runs) and less predictable.
    - **Stage 6 (Pipeline Agent)**: Uses deterministic code (keyword router) to call tools *before* calling the LLM. It is fast, predictable, and makes only one LLM call—making it the industry-standard architecture for enterprise web-search and copilot agents.
* **Q: How does this scale to a production app?**
  * **A**: To make this production-ready:
    1. Swap the keyword router with a semantic router (or an LLM-based tool-calling router).
    2. Save session history and resumes to a database.
    3. Implement RAG using a vector database (e.g., ChromaDB or Pinecone) to search matching jobs from a private database.

---

## 🌟 Advanced Extension: Adding More Tools (Skills Gap Analyzer)
We have added a second, local python tool inside `ai/tools.py` called **`analyze_skills_gap(background, job_description)`** that compares the user's copy-pasted background text against a job description.

### 🛠️ How it works:
* It does not make any network or LLM requests. It uses Python to intersect common tech skills (e.g., python, sql, tensorflow) between the background and the listing description.
* Returns a dictionary: `{"match_score": int, "matching_skills": list, "missing_skills": list}`.

### 🎓 Teaching Point:
* Use this to show students how we transition from a **single-tool agent** to a **multi-tool agent**. 
* Students can extend the ReAct prompt (`REACT_SYSTEM`) in Stage 4 to declare:
  > `analyze_skills_gap(background, job_description) — compares your background skills against a job description text, returning a match score (0-100%) and missing skills.`
* They can observe the agent first run a search query, and then run `analyze_skills_gap` to assess matching scores before giving its `Final Answer`.
