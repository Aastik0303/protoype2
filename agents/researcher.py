import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
from langchain.schema import HumanMessage, SystemMessage
from utils.llm import stream

SYSTEM = """You are a research analyst. Synthesize web sources into a clear, structured report.
Use markdown with headers and bullet points. Cite sources. Be factual and concise."""


def _search(query: str) -> list:
    try:
        from duckduckgo_search import DDGS
        with DDGS() as d:
            return list(d.text(query, max_results=5))
    except Exception:
        return []


def _scrape(url: str) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
        soup = BeautifulSoup(r.text, "html.parser")
        for t in soup(["script", "style", "nav", "header", "footer"]):
            t.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]
    except Exception:
        return ""


def run(message: str, history: list):
    yield f"🔍 Searching for: **{message}**\n\n"

    results = _search(message)

    if not results:
        yield "⚠️ Web search unavailable. Answering from knowledge...\n\n---\n\n"
        yield from stream([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=f"Answer this research question thoroughly:\n\n{message}"),
        ], temperature=0.4)
        return

    yield f"📄 Found {len(results)} sources — reading...\n\n"

    scraped = []
    for i, r in enumerate(results[:4], 1):
        url   = r.get("href", "")
        title = r.get("title", "Unknown")
        body  = r.get("body", "")
        content = _scrape(url) if url else body
        scraped.append(f"**Source {i}: {title}**\nURL: {url}\n{content or body}")
        yield f"✅ Read source {i}: {title[:50]}\n"

    yield "\n---\n\n🧠 Writing report...\n\n"

    prompt = f"""Research Query: {message}

Sources:
{'---'.join(scraped)}

Write a clear research report:
## Summary
## Key Findings
## Sources"""

    yield from stream([
        SystemMessage(content=SYSTEM),
        HumanMessage(content=prompt),
    ], temperature=0.3)
