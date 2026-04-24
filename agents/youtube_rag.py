import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
from utils.llm import stream
from utils.embeddings import get_embeddings

_vectorstore = None
_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)


def _get_video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot find video ID in: {url}")


def _fetch_transcript(video_id: str) -> str:
    # Method 1: youtube-transcript-api
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        data = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["en", "en-US", "en-GB", "a.en"]
        )
        return " ".join(d["text"] for d in data)
    except Exception as e1:
        pass

    # Method 2: scrape caption track from page
    try:
        import requests, json, html as htmllib
        resp = requests.get(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        m = re.search(r'"captionTracks":\s*(\[.*?\])', resp.text)
        if m:
            tracks = json.loads(m.group(1))
            url = next(
                (t["baseUrl"] for t in tracks if "en" in t.get("languageCode", "")),
                tracks[0]["baseUrl"] if tracks else None,
            )
            if url:
                xml = requests.get(url, timeout=8).text
                texts = re.findall(r"<text[^>]*>(.*?)</text>", xml, re.DOTALL)
                return " ".join(
                    htmllib.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in texts
                )
    except Exception as e2:
        pass

    raise RuntimeError("Could not fetch transcript. The video may not have captions.")


def ingest(url: str) -> str:
    global _vectorstore
    vid = _get_video_id(url)
    transcript = _fetch_transcript(vid)
    doc = Document(page_content=transcript, metadata={"source": url})
    chunks = _splitter.split_documents([doc])
    _vectorstore = FAISS.from_documents(chunks, get_embeddings())
    return f"✅ Video loaded — {len(chunks)} transcript chunks indexed. Now ask questions!"


def run(message: str, history: list):
    if not _vectorstore:
        yield "⚠️ No video loaded. Paste a YouTube URL in the sidebar and click **Load Video**."
        return
    docs = _vectorstore.similarity_search(message, k=5)
    context = "\n\n".join(d.page_content for d in docs)
    prompt = f"""You are analyzing a YouTube video transcript. Answer based on the content.

Transcript:
{context}

Question: {message}"""
    yield from stream([HumanMessage(content=prompt)], temperature=0.3)
