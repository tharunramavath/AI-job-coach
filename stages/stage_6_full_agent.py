import os
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


SEARCH_KEYWORDS = [
    "find", "search", "job", "opening", "hiring", "role",
    "vacancy", "position", "listing", "apply",
]

def should_search(query: str) -> bool:
    """Decides if the query contains job search keywords."""
    q = query.lower()
    return any(kw in q for kw in SEARCH_KEYWORDS)


def search_jobs(query: str, num_results: int = 5) -> list[dict]:
    """Search for real job listings using Jina Search API."""
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        raise ValueError("JINA_API_KEY not set in .env")

    search_query = f'site:linkedin.com/jobs/view/ OR site:naukri.com/job-listings/ OR site:indeed.com/viewjob "{query}"'
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "X-With-Generated-Alt": "true",
    }

    response = requests.get(
        "https://s.jina.ai/" + requests.utils.quote(search_query),
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("data", [])[:num_results]:
        results.append({
            "title": item.get("title", "No title"),
            "url": item.get("url", ""),
            "snippet": item.get("description", item.get("content", ""))[:300],
        })
    return results


COMMON_SKILLS = [
    "python", "machine learning", "deep learning", "tensorflow", "pytorch",
    "sql", "react", "javascript", "docker", "kubernetes", "aws", "gcp",
    "azure", "java", "c++", "data engineering", "nlp", "computer vision",
    "spark", "tableau", "excel", "git", "rest api", "django", "flask", "fastapi"
]

def analyze_skills_gap(background: str, job_description: str) -> dict:
    """
    Compares user background skills against a job description.
    Returns matching score (0-100), matching skills, and missing skills.
    """
    bg_lower = background.lower() if background else ""
    jd_lower = job_description.lower()
    
    user_skills = [skill for skill in COMMON_SKILLS if skill in bg_lower]
    required_skills = [skill for skill in COMMON_SKILLS if skill in jd_lower]
    
    if not required_skills:
        return {
            "match_score": 100,
            "matching_skills": user_skills,
            "missing_skills": []
        }
        
    matching = [skill for skill in required_skills if skill in user_skills]
    missing = [skill for skill in required_skills if skill not in user_skills]
    
    score = int((len(matching) / len(required_skills)) * 100)
    
    return {
        "match_score": score,
        "matching_skills": matching,
        "missing_skills": missing
    }


def format_jobs(jobs: list[dict], resume: str = "") -> str:
    """Format job results into a clean string for the LLM context, showing matching scores."""
    if not jobs:
        return "No jobs found."
    lines = []
    for i, job in enumerate(jobs, 1):
        lines.append(f"{i}. {job['title']}")
        lines.append(f"   URL: {job['url']}")
        
        # Analyze skills gap if resume is provided
        if resume:
            analysis = analyze_skills_gap(resume, job['title'] + " " + job['snippet'])
            lines.append(f"   Match Score: {analysis['match_score']}%")
            lines.append(f"   Matching Skills: {', '.join(analysis['matching_skills']) if analysis['matching_skills'] else 'None'}")
            lines.append(f"   Missing Skills: {', '.join(analysis['missing_skills']) if analysis['missing_skills'] else 'None'}")
            
        lines.append(f"   Description: {job['snippet']}")
        lines.append("")
    return "\n".join(lines)


def summarize_preferences(history: list[dict]) -> str:
    """Extracts key preferences mentioned by the user from conversation history."""
    if not history:
        return ""
    user_turns = [m["content"] for m in history if m["role"] == "user"]
    if not user_turns:
        return ""
    combined = "\n".join(f"- {t}" for t in user_turns[-10:])  # last 10 user messages
    return f"Previous things the user said:\n{combined}"


def chat_stream(messages: list[dict], system: str = None, temperature: float = 0.7):
    """Helper to stream from Groq LLaMA directly."""
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please enter it in the sidebar.")
    model = st.session_state.get("groq_model") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    client = Groq(api_key=api_key)
    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    
    response_stream = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=1024,
        stream=True
    )
    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def run_stage_6_stream(user_input: str, resume: str, history: list[dict]) -> tuple[str, any]:
    """
    Runs the full agent step, decision, tool invocation, and yields the LLM response stream.
    Returns:
        tuple: (tool_context, stream_generator)
    """
    tool_context = ""
    if should_search(user_input):
        try:
            jobs = search_jobs(user_input, num_results=5)
            tool_context = format_jobs(jobs, resume)
        except Exception as e:
            tool_context = f"Search failed: {e}"
            
    preferences = summarize_preferences(history)
    
    system = f"""You are a personalized AI job coach. You have three capabilities:
1. You know the user's background and preferences from their resume
2. You can access real-time job listings (provided below if a search was done)
3. You remember everything the user has said in this conversation

User resume:
{resume if resume else "Not provided yet — ask the user to paste their resume."}

{preferences}

{f"Real job listings found:{chr(10)}{tool_context}" if tool_context else ""}

Give specific, actionable advice. Reference the user's actual background and the real listings when relevant."""

    # Build messages for LLM (filter user and assistant turns)
    llm_messages = [m for m in history if m["role"] in ("user", "assistant")]
    
    return tool_context, chat_stream(messages=llm_messages, system=system)

