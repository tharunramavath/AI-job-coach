import os
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


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
    bg_lower = background.lower()
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


def format_jobs(jobs: list[dict], resume_snippet: str = "") -> str:
    """Format job results into a clean string for the LLM context, showing matching scores."""
    if not jobs:
        return "No jobs found."
    lines = []
    for i, job in enumerate(jobs, 1):
        lines.append(f"{i}. {job['title']}")
        lines.append(f"   URL: {job['url']}")
        
        # Analyze skills gap if background is provided
        if resume_snippet:
            analysis = analyze_skills_gap(resume_snippet, job['title'] + " " + job['snippet'])
            lines.append(f"   Match Score: {analysis['match_score']}%")
            lines.append(f"   Matching Skills: {', '.join(analysis['matching_skills']) if analysis['matching_skills'] else 'None'}")
            lines.append(f"   Missing Skills: {', '.join(analysis['missing_skills']) if analysis['missing_skills'] else 'None'}")
            
        lines.append(f"   Description: {job['snippet']}")
        lines.append("")
    return "\n".join(lines)


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


def run_stage_3(role_query: str, resume_snippet: str) -> dict:
    """Performs a real-time job search and synthesizes context-aware advice."""
    jobs = search_jobs(role_query, num_results=5)
    jobs_text = format_jobs(jobs, resume_snippet)
    
    system = """You are a job search assistant. The user has provided their background and you've been given real job listings from the web along with matching metrics.
Analyze the listings and matching scores, and give specific, actionable advice: which roles match, which to prioritize, what to highlight in applications, and how to bridge any skills gaps."""

    user_message = f"""User background: {resume_snippet if resume_snippet else "Not provided"}

Real job listings and matching analysis found:
{jobs_text}

Based on these real listings, what should I do next?"""

    response = chat(
        messages=[{"role": "user", "content": user_message}],
        system=system,
    )
    
    return {
        "jobs_text": jobs_text,
        "response": response
    }

