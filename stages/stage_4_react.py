import os
import re
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def search_jobs(query: str, num_results: int = 4) -> list[dict]:
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


def format_jobs(jobs: list[dict]) -> str:
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


REACT_SYSTEM = """You are a job search assistant that reasons step by step before acting.

You have access to one tool:
  search_jobs(query) — searches the web for real job listings

To use the tool, respond in this EXACT format:
  Thought: <your reasoning about what to do>
  Action: search_jobs("<search query>")

When you have enough information to answer, respond in this EXACT format:
  Thought: <your reasoning>
  Final Answer: <your answer to the user>

Rules:
- Always start with a Thought
- Only call search_jobs when you need CURRENT job listings
- Never execute the exact same search query twice. If you need more information, vary your search keywords (e.g. add tech stack details, experience requirements, or query synonyms).
- If the user asks something factual or about their profile, answer directly without searching
- Be concise in your thoughts
"""


def run_stage_4(user_query: str, resume_context: str = "") -> list[dict]:
    """
    Runs the self-contained ReAct loop.
    Returns:
        list of dicts tracing the execution:
        [{"type": "thought"|"action"|"observation"|"final", "content": str}]
    """
    steps = []
    messages = [{"role": "user", "content": user_query}]
    executed_queries = set()

    system = REACT_SYSTEM
    if resume_context:
        system += f"\n\nUser background:\n{resume_context}"

    max_iterations = 4
    for _ in range(max_iterations):
        response = chat(messages, system=system, temperature=0.3)
        messages.append({"role": "assistant", "content": response})

        # Parse Thought
        thought_match = re.search(r"Thought:\s*(.+?)(?=Action:|Final Answer:|$)", response, re.DOTALL)
        if thought_match:
            steps.append({"type": "thought", "content": thought_match.group(1).strip()})

        # Check for Final Answer
        final_match = re.search(r"Final Answer:\s*(.+)", response, re.DOTALL)
        if final_match:
            steps.append({"type": "final", "content": final_match.group(1).strip()})
            break

        # Check for Action
        action_match = re.search(r'Action:\s*search_jobs\(["\'](.+?)["\']\)', response)
        if action_match:
            query = action_match.group(1).strip()
            steps.append({"type": "action", "content": f'search_jobs("{query}")'})

            # Handle duplicate query loop prevention
            if query.lower() in executed_queries:
                observation = f"Observation: You have already searched for '{query}'. To avoid looping, please try a different, more specific query with different keywords, or summarize your findings and provide your Final Answer now."
            else:
                executed_queries.add(query.lower())
                # Execute search
                try:
                    jobs = search_jobs(query, num_results=4)
                    observation = format_jobs(jobs)
                except Exception as e:
                    observation = f"Search failed: {str(e)}"

            steps.append({"type": "observation", "content": observation})
            messages.append({"role": "user", "content": f"Observation:\n{observation}\n\nContinue."})
        else:
            # No action found — treat the whole response as final
            steps.append({"type": "final", "content": response})
            break

    # Fallback: if the loop completed all iterations but no final answer was logged
    has_final = any(step["type"] == "final" for step in steps)
    if not has_final:
        # Request a final answer forcing the agent to summarize
        messages.append({
            "role": "user",
            "content": "You have reached the maximum allowed reasoning steps. Please synthesize all thoughts and observations so far and provide your Final Answer to the user now."
        })
        try:
            fallback_response = chat(messages, system=system, temperature=0.3)
            final_match = re.search(r"Final Answer:\s*(.+)", fallback_response, re.DOTALL)
            if final_match:
                steps.append({"type": "final", "content": final_match.group(1).strip()})
            else:
                clean_res = fallback_response.replace("Thought:", "").replace("Final Answer:", "").strip()
                steps.append({"type": "final", "content": clean_res})
        except Exception as e:
            steps.append({"type": "final", "content": f"Failed to generate final answer: {e}"})

    return steps

