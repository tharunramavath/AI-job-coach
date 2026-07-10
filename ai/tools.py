import os
import requests
from dotenv import load_dotenv

load_dotenv()

JINA_BASE = "https://s.jina.ai/"


def search_jobs(query: str, num_results: int = 5) -> list[dict]:
    """
    Search for real job listings using Jina Search API.
    Returns a list of job result dicts with title, url, snippet.
    """
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        raise ValueError("JINA_API_KEY not set in .env")

    search_query = (
        f'site:linkedin.com/jobs/view/ OR site:naukri.com/job-listings/ OR site:indeed.com/viewjob {query}'
    )


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-With-Generated-Alt": "true",
    }

    response = requests.post(
        "https://s.jina.ai",
        headers=headers,
        json={"q": search_query},
        timeout=30,
    )
    if response.status_code == 422:
        return []
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("data", [])[:num_results]:
        results.append(
            {
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "snippet": item.get("description", item.get("content", ""))[:300],
            }
        )

    return results


def format_jobs_for_llm(jobs: list[dict]) -> str:
    """Format job results into a clean string for the LLM context."""
    if not jobs:
        return "No jobs found."
    lines = []
    for i, job in enumerate(jobs, 1):
        lines.append(f"{i}. {job['title']}")
        lines.append(f"   URL: {job['url']}")
        lines.append(f"   {job['snippet']}")
        lines.append("")
    return "\n".join(lines)


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

