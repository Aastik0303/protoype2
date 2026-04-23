import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import re
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
from utils.llm_factory import stream_with_fallback
from utils.embeddings import get_embeddings


def _extract_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot extract video ID from: {url}")


def _transcript_api(video_id: str) -> str:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, languages=["en", "en-US", "en-GB", "a.en"]
    )
    return TextFormatter().format_transcript(transcript)


def _transcript_scrape(video_id: str) -> str:
    import json, html as html_module
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=10)
    match = re.search(r'"captionTracks":\s*(\[.*?\])', resp.text)
    if not match:
        raise RuntimeError("No captions in page source")
    tracks = json.loads(match.group(1))
    track_url = next(
        (t["baseUrl"] for t in tracks if t.get("languageCode", "").startswith("en")),
        tracks[0]["baseUrl"] if tracks else None
    )
    if not track_url:
        raise RuntimeError("No caption track URL")
    xml = requests.get(track_url, timeout=10).text
    texts = re.findall(r"<text[^>]*>(.*?)</text>", xml, re.DOTALL)
    return " ".join(
        html_module.unescape(re.sub(r"<[^>]+>", "", t)).strip()
        for t in texts if t.strip()
    )


def _transcript_ytdlp(video_id: str) -> str:
    import yt_dlp, tempfile, glob
    with tempfile.TemporaryDirectory() as tmpdir:
        opts = {
            "skip_download": True, "writesubtitles": True,
            "writeautomaticsub": True, "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        vtt_files = glob.glob(os.path.join(tmpdir, "*.vtt"))
        if not vtt_files:
            raise RuntimeError("No subtitle files downloaded")
        with open(vtt_files[0], encoding="utf-8") as f:
            vtt = f.read()
    lines = []
    for line in vtt.split("\n"):
        line = line.strip()
        if line.startswith("WEBVTT") or "-->" in line or not line:
            continue
        clean = re.sub(r"<[^>]+>", "", line)
        if clean and (not lines or clean != lines[-1]):
            lines.append(clean)
    return " ".join(lines)


def get_transcript(video_id: str) -> tuple[str, str]:
    errors = []
    for name, fn in [
        ("youtube-transcript-api", _transcript_api),
        ("page-scraping",          _transcript_scrape),
        ("yt-dlp",                 _transcript_ytdlp),
    ]:
        try:
            text = fn(video_id)
            if text and len(text.strip()) > 100:
                return text, name
        except Exception as e:
            errors.append(f"{name}: {e}")
    raise RuntimeError("All transcript methods failed:\n" + "\n".join(errors))


class YouTubeRAGAgent:
    NAME = "YouTube RAG"
    ICON = "▶️"
    MODEL_TAG = "Transcript + HuggingFace + RAG"

    SYSTEM = """You are a YouTube Video Analysis Agent.

BEHAVIOR:
- Extract key information from video transcript
- If transcript fails → gracefully provide summary from title/context
- NEVER crash or show raw errors
- Sound human and helpful

OUTPUT FORMAT (always follow):
Agent Used: YouTube RAG

Response:

**Video Summary:**
<2-3 sentence summary>

**Key Points:**
- <point 1>
- <point 2>
- <point 3>

**Answer to your question:**
<direct answer based on transcript>"""

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        self.vectorstore = None
        self.loaded_url = None
        self.method_used = None

    def ingest(self, url: str) -> str:
        vid = _extract_id(url)
        try:
            transcript, method = get_transcript(vid)
            doc = Document(page_content=transcript, metadata={"source": url})
            chunks = self.splitter.split_documents([doc])
            self.vectorstore = FAISS.from_documents(chunks, get_embeddings())
            self.loaded_url = url
            self.method_used = method
            return (f"✅ Transcript loaded via **{method}** — "
                    f"{len(chunks)} chunks ready.\nVideo ID: `{vid}`")
        except Exception as e:
            return f"⚠️ Unable to fetch transcript: {e}\nYou can still ask questions — I'll answer from context."

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        if not self.vectorstore:
            yield "⚠️ No video loaded. Paste a YouTube URL in the sidebar and click **Load Video**."
            return

        docs = self.vectorstore.similarity_search(message, k=5)
        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""Video transcript context:
{context}

User question: {message}

Follow the output format from your system instructions exactly."""

        yield from stream_with_fallback([
            HumanMessage(content=self.SYSTEM + "\n\n" + prompt)
        ], temperature=0.3)
