"""Core RAG logic for Suraksha-RAG (shared by build_index.py, app.py, evaluate.py)."""
import os
from pathlib import Path

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_DIR = Path(__file__).parent / "faiss_index"

# Multilingual model: understands English, Hindi, Kannada, etc.
# Runs on ONNX via fastembed (no PyTorch needed -> light enough for Streamlit Cloud).
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

TOP_K = 6
NOT_FOUND = "NOT_FOUND"
LANG_NAMES = {"en": "English", "hi": "Hindi", "kn": "Kannada"}

PROMPT = """You are Suraksha, an industrial workplace safety assistant for factories in India.

RULES
1. Answer ONLY using the CONTEXT below. Never use outside knowledge. Never guess.
2. Give short, numbered, imperative steps a worker can follow quickly (maximum 8 steps).
3. After each step, cite the context number in square brackets, like [1] or [2].
4. If the CONTEXT contains nothing relevant to the QUESTION, reply with exactly: NOT_FOUND.
   If it covers only part of the question, give only what it states and say which part is not covered.
5. Write the answer in {language}. Keep numbers, legal section numbers and citation numbers [n] unchanged.
6. Do not add warnings or disclaimers; the app shows them separately.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


def get_secret(name, default=None):
    """Read a key from environment variables or Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(name, default)
    except Exception:
        return default


def get_embeddings():
    return FastEmbedEmbeddings(model_name=EMBED_MODEL)


def load_index():
    if not (INDEX_DIR / "index.faiss").exists():
        raise FileNotFoundError(
            "faiss_index/ not found. Put PDFs in data/ and run: python build_index.py"
        )
    # allow_dangerous_deserialization is safe here: we load only an index we built ourselves.
    return FAISS.load_local(
        str(INDEX_DIR), get_embeddings(), allow_dangerous_deserialization=True
    )


def get_llm():
    from langchain_groq import ChatGroq

    api_key = get_secret("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing (set it in .streamlit/secrets.toml or env).")
    model = get_secret("GROQ_MODEL", "openai/gpt-oss-120b")
    return ChatGroq(model=model, temperature=0, api_key=api_key, max_retries=2)


def answer_question(question, lang, store, llm):
    """Retrieve top chunks, ask the LLM, return a dict the UI can render."""
    docs = store.similarity_search(question, k=TOP_K)

    context_parts, sources = [], []
    for i, d in enumerate(docs, start=1):
        name = d.metadata.get("source_name", "manual")
        page = d.metadata.get("page_no", "?")
        context_parts.append(f"[{i}] (Source: {name}, page {page})\n{d.page_content}")
        sources.append({"n": i, "name": name, "page": page, "text": d.page_content})

    prompt = PROMPT.format(
        language=LANG_NAMES.get(lang, "English"),
        context="\n\n".join(context_parts),
        question=question,
    )
    text = llm.invoke(prompt).content.strip()
    found = NOT_FOUND not in text[:30]
    return {"answer": text if found else "", "found": found, "sources": sources}
