import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import requests
import time
from bs4 import BeautifulSoup
from langchain.schema import HumanMessage, SystemMessage
from utils.llm_factory import stream_with_fallback


SYSTEM = """You are an expert research analyst and report writer.
You receive web search results and synthesize them into a comprehensive, well-structured markdown report.
Always cite sources, highlight key insights, and write in a clear, professional style."""


def _search_duckduckgo(query: str, n: int = 6) -> list:
    """DuckDuckGo search with retry logic."""
    for attempt in range(3):
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=n))
            if results:
                return results
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
    return []


def _search_google_fallback(query: str, n: int = 5) -> list:
    """Google search fallback via googlesearch-python."""
    try:
        from googlesearch import search
        results = []
        for url in search(query, num_results=n, sleep_interval=1):
            results.append({"href": url, "title": url, "body": ""})
        return results
    except Exception:
        return []


def _search_direct_fallback(query: str) -> list:
    """Last resort: hardcoded Wikipedia + news search."""
    try:
        encoded = requests.utils.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded}&limit=3&format=json"
        resp = requests.get(url, timeout=8)
        data = resp.json()
        results = []
        for title, link in zip(data[1], data[3]):
            results.append({"href": link, "title": title, "body": ""})
        return results
    except Exception:
        return []


def web_search(query: str) -> list:
    """Search with multiple fallbacks: DDG → Google → Wikipedia."""
    results = _search_duckduckgo(query)
    if results:
        return results
    results = _search_google_fallback(query)
    if results:
        return results
    return _search_direct_fallback(query)


def scrape(url: str, max_chars: int = 2500) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=7)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:max_chars]
    except Exception:
        return ""


class DeepResearcherAgent:
    NAME = "Deep Researcher"
    ICON = "🔬"
    MODEL_TAG = "Web Search + Gemini/Groq Synthesis"

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        yield f"🔍 **Researching:** {message}\n\n"
        yield "📡 Searching the web (DDG → Google → Wikipedia fallback)...\n\n"

        results = web_search(message)

        if not results:
            # Fallback: answer from LLM knowledge directly
            yield "⚠️ Web search unavailable. Answering from model knowledge...\n\n---\n\n"
            prompt = f"""The web search is unavailable right now. 
Please answer this research question as thoroughly as possible from your training knowledge.
Include key facts, context, and insights.

Research Question: {message}

Format your answer as a structured report with sections."""
            yield from stream_with_fallback([
                SystemMessage(content=SYSTEM),
                HumanMessage(content=prompt),
            ], temperature=0.4)
            return

        yield f"✅ Found **{len(results)} sources** — reading content...\n\n"

        scraped = []
        for i, r in enumerate(results[:5], 1):
            url   = r.get("href", "")
            title = r.get("title", "Unknown")
            body  = r.get("body", "")
            yield f"📄 Source {i}: *{title[:65]}*\n"
            content = scrape(url) if url else body
            scraped.append({
                "title": title,
                "url":   url,
                "content": content or body or "No content available",
            })

        yield "\n---\n\n🧠 **Synthesizing research report...**\n\n"

        sources_block = "\n\n".join(
            f"**[Source {i+1}]** {s['title']}\n"
            f"URL: {s['url']}\n"
            f"Content: {s['content']}"
            for i, s in enumerate(scraped)
        )

        prompt = f"""Research Query: {message}

Web Sources Collected:
{sources_block}

Write a comprehensive, well-structured research report with the following sections:

## 📋 Executive Summary
## 🔑 Key Findings
## 📊 Detailed Analysis
## 🔗 Sources & References  
## ✅ Conclusion

Use markdown formatting, bullet points, and clear headings."""

        yield from stream_with_fallback([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=prompt),
        ], temperature=0.4)
