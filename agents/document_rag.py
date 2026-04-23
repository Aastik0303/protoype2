import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
from utils.llm_factory import stream_with_fallback
from utils.embeddings import get_embeddings

try:
    import docx2txt
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class DocumentRAGAgent:
    NAME = "Document RAG"
    ICON = "📄"
    MODEL_TAG = "HuggingFace Embeddings + FAISS"

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        self.vectorstore = None

    def ingest(self, uploaded_file) -> str:
        suffix = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(uploaded_file.read())
            tmp = f.name
        try:
            if suffix == ".pdf":
                docs = PyPDFLoader(tmp).load()
            elif suffix == ".docx" and HAS_DOCX:
                text = docx2txt.process(tmp)
                docs = [Document(page_content=text, metadata={"source": uploaded_file.name})]
            else:
                docs = TextLoader(tmp, encoding="utf-8").load()

            chunks = self.splitter.split_documents(docs)
            emb = get_embeddings()
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
            else:
                self.vectorstore = FAISS.from_documents(chunks, emb)
            return f"✅ **{uploaded_file.name}** ingested — {len(chunks)} chunks indexed with HuggingFace embeddings."
        finally:
            os.unlink(tmp)

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        if not self.vectorstore:
            yield "⚠️ No documents loaded. Upload a PDF, TXT, or DOCX in the sidebar."
            return
        docs = self.vectorstore.similarity_search(message, k=4)
        context = "\n\n".join(d.page_content for d in docs)
        prompt = f"""Answer based only on the document context below.
If the answer is not found in the context, clearly say so.

Document Context:
{context}

Question: {message}"""
        yield from stream_with_fallback([HumanMessage(content=prompt)], temperature=0.2)
