import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
from utils.llm import stream
from utils.embeddings import get_embeddings

try:
    import docx2txt
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

_vectorstore = None
_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)


def ingest(uploaded_file) -> str:
    global _vectorstore
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
        chunks = _splitter.split_documents(docs)
        emb = get_embeddings()
        if _vectorstore:
            _vectorstore.add_documents(chunks)
        else:
            _vectorstore = FAISS.from_documents(chunks, emb)
        return f"✅ **{uploaded_file.name}** indexed — {len(chunks)} chunks ready."
    finally:
        os.unlink(tmp)


def run(message: str, history: list):
    if not _vectorstore:
        yield "⚠️ No document loaded. Please upload a PDF, TXT, or DOCX in the sidebar first."
        return
    docs = _vectorstore.similarity_search(message, k=4)
    context = "\n\n".join(d.page_content for d in docs)
    prompt = f"""Answer the question using only the document context below.
If the answer is not in the context, say so clearly.

Context:
{context}

Question: {message}"""
    yield from stream([HumanMessage(content=prompt)], temperature=0.2)
