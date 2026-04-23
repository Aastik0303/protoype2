import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import requests
import time
from bs4 import BeautifulSoup
from langchain.schema import HumanMessage, SystemMessage
from utils.llm_factory import stream_with_fallback


SYSTEM = """You are a Fast, Smart Deep Research Agent.

BEHAVIOR RULES:
- Keep research FAST and FOCUSED
- Maximum 3 reasoning steps
- Avoid unnecessary exploration
- Never expose raw errors — always give alternative answer

OUTPUT FORMAT (always follow this):
Agent Used: Deep Researcher

Response:

**Direct Answer:**
<answer here>

**Key Explanation:**
<brief explanation>

**Quick Insight:**
<optional short insight>

---
*Sources used: <number> web sources*"""


def _search_duckduckgo(query: str, n: int = 6) -> list:
    for attempt in range(3):
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=n))
            if results:
                return results
        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)
    return []


def _search_google_fallback(query: str, n: int = 5) -> list:
    try:
        from googlesearch import search
        results = []
        for url in search(query, num_results=n, sleep_interval=1):
            results.append({"href": url, "title": url, "body": ""})
        return results
    except Exception:
        return []


def _wikipedia_fallback(query: str) -> list:
    try:
        encoded = requests.utils.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded}&limit=3&format=json"
        resp = requests.get(url, timeout=8)
        data = resp.json()
        return [{"href": link, "title": title, "body": ""}
                for title, link in zip(data[1], data[3])]
    except Exception:
        return []


def web_search(query: str) -> list:
    results = _search_duckduckgo(query)
    if results:
        return results
    results = _search_google_fallback(query)
    if results:
        return results
    return _wikipedia_fallback(query)


def scrape(url: str, max_chars: int = 2000) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:max_chars]
    except Exception:
        return ""


class DeepResearcherAgent:
    NAME = "Deep Researcher"
    ICON = "🔬"
    MODEL_TAG = "Web Search + Gemini/Groq Synthesis"

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        yield f"🔍 Searching for: **{message}**\n\n"

        results = web_search(message)

        if not results:
            yield "⚠️ Web search unavailable — answering from model knowledge...\n\n---\n\n"
            prompt = f"""Web search failed. Answer this research question from your knowledge.
Be structured and concise. Maximum 3 key points.

Research Question: {message}

Follow this format exactly:
Agent Used: Deep Researcher

Response:

**Direct Answer:**
<answer>

**Key Explanation:**
<explanation>

**Quick Insight:**
<insight>"""
            yield from stream_with_fallback([
                SystemMessage(content=SYSTEM),
                HumanMessage(content=prompt),
            ], temperature=0.3)
            return

        yield f"✅ Found **{len(results)} sources** — synthesizing...\n\n"

        scraped = []
        for i, r in enumerate(results[:4], 1):
            url     = r.get("href", "")
            title   = r.get("title", "Unknown")
            body    = r.get("body", "")
            content = scrape(url) if url else body
            scraped.append({
                "title":   title,
                "url":     url,
                "content": content or body or "No content",
            })

        yield "🧠 **Writing research report...**\n\n---\n\n"

        sources_block = "\n\n".join(
            f"[Source {i+1}] {s['title']}\nURL: {s['url']}\nContent: {s['content']}"
            for i, s in enumerate(scraped)
        )

        prompt = f"""Research Query: {message}

Sources:
{sources_block}

Write a fast, focused research response.
Follow this format exactly:

Agent Used: Deep Researcher

Response:

**Direct Answer:**
<2-3 sentence direct answer>

**Key Explanation:**
<bullet points of key findings>

**Quick Insight:**
<one valuable insight>

---
*Sources used: {len(scraped)} web sources*"""

        yield from stream_with_fallback([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=prompt),
        ], temperature=0.3)
