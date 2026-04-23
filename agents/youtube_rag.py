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


def _get_transcript_primary(video_id: str) -> str:
    """Method 1: youtube-transcript-api"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "en-US", "en-GB", "a.en"]
        )
        return TextFormatter().format_transcript(transcript)
    except Exception as e:
        raise RuntimeError(f"transcript-api failed: {e}")


def _get_transcript_scrape(video_id: str) -> str:
    """Method 2: Scrape timedtext from YouTube's internal API"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=10)
        html = resp.text

        # Find timedtext URL in page source
        import json
        match = re.search(r'"captionTracks":\s*(\[.*?\])', html)
        if not match:
            raise RuntimeError("No captions found in page source")

        tracks = json.loads(match.group(1))
        # Prefer English
        track_url = None
        for track in tracks:
            if track.get("languageCode", "").startswith("en"):
                track_url = track["baseUrl"]
                break
        if not track_url and tracks:
            track_url = tracks[0]["baseUrl"]
        if not track_url:
            raise RuntimeError("No caption track URL found")

        xml_resp = requests.get(track_url, timeout=10)
        # Parse XML captions
        texts = re.findall(r"<text[^>]*>(.*?)</text>", xml_resp.text, re.DOTALL)
        import html as html_module
        clean = [html_module.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in texts]
        return " ".join(filter(None, clean))
    except Exception as e:
        raise RuntimeError(f"scrape failed: {e}")


def _get_transcript_ytdlp(video_id: str) -> str:
    """Method 3: yt-dlp subtitles"""
    try:
        import yt_dlp
        import tempfile, json, glob

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en", "en-US"],
                "subtitlesformat": "vtt",
                "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
                "quiet": True,
            }
            url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            vtt_files = glob.glob(os.path.join(tmpdir, "*.vtt"))
            if not vtt_files:
                raise RuntimeError("No subtitle files downloaded")

            with open(vtt_files[0], encoding="utf-8") as f:
                vtt = f.read()

            # Strip VTT tags and timestamps
            lines = []
            for line in vtt.split("\n"):
                line = line.strip()
                if line.startswith("WEBVTT") or "-->" in line or not line:
                    continue
                clean = re.sub(r"<[^>]+>", "", line)
                if clean and clean not in lines[-3:] if lines else True:
                    lines.append(clean)
            return " ".join(lines)
    except Exception as e:
        raise RuntimeError(f"yt-dlp failed: {e}")


def get_transcript(video_id: str) -> tuple[str, str]:
    """Try all methods in order, return (transcript_text, method_used)."""
    errors = []

    for method_name, method_fn in [
        ("youtube-transcript-api", _get_transcript_primary),
        ("page-scraping",          _get_transcript_scrape),
        ("yt-dlp",                 _get_transcript_ytdlp),
    ]:
        try:
            text = method_fn(video_id)
            if text and len(text.strip()) > 100:
                return text, method_name
        except Exception as e:
            errors.append(f"{method_name}: {e}")

    raise RuntimeError(
        "All transcript methods failed:\n" + "\n".join(errors)
    )


class YouTubeRAGAgent:
    NAME = "YouTube RAG"
    ICON = "▶️"
    MODEL_TAG = "HuggingFace Embeddings + Transcript"

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        self.vectorstore = None
        self.loaded_url = None
        self.method_used = None

    def ingest(self, url: str) -> str:
        vid = _extract_id(url)
        transcript, method = get_transcript(vid)
        doc = Document(page_content=transcript, metadata={"source": url, "video_id": vid})
        chunks = self.splitter.split_documents([doc])
        self.vectorstore = FAISS.from_documents(chunks, get_embeddings())
        self.loaded_url = url
        self.method_used = method
        return (f"✅ YouTube transcript loaded via **{method}** — "
                f"{len(chunks)} chunks indexed.\n"
                f"Video: `{vid}`")

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        if not self.vectorstore:
            yield "⚠️ No video loaded. Paste a YouTube URL in the sidebar and click **Load Video**."
            return
        docs = self.vectorstore.similarity_search(message, k=5)
        context = "\n\n".join(d.page_content for d in docs)
        prompt = f"""You are analyzing a YouTube video transcript. Answer the question based on what was said.

Transcript Excerpts:
{context}

Question: {message}

Give a clear, detailed answer based on the video content."""
        yield from stream_with_fallback([HumanMessage(content=prompt)], temperature=0.3)
