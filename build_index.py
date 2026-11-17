"""Run ONCE on your laptop (and again whenever you add/change PDFs):
    python build_index.py
Then commit the faiss_index/ folder to GitHub.
"""
import re
import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

import rag

DATA_DIR = Path(__file__).parent / "data"


def clean(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"-\n(\w)", r"\1", text)      # re-join words hyphenated at line end
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    pdfs = list(DATA_DIR.rglob("*.pdf"))
    if not pdfs:
        sys.exit("No PDFs found in data/. Add your safety manuals there first.")
    print(f"Found {len(pdfs)} PDF(s): {[p.name for p in pdfs]}")

    pages = PyPDFDirectoryLoader(str(DATA_DIR), recursive=True).load()

    docs, empty = [], 0
    for p in pages:
        p.page_content = clean(p.page_content)
        if len(p.page_content) < 40:      # blank / scanned page
            empty += 1
            continue
        p.metadata["source_name"] = Path(p.metadata.get("source", "manual")).stem
        p.metadata["page_no"] = int(p.metadata.get("page", 0)) + 1   # 1-based for humans
        docs.append(p)
    print(f"Loaded {len(docs)} text pages ({empty} empty/scanned pages skipped).")
    if empty > len(pages) * 0.3:
        print("WARNING: many pages had no text. Those PDFs may be scanned and need OCR.")
    if not docs:
        sys.exit("No extractable text. Use text-based PDFs (or run OCR first).")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", "; ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks. Embedding (first run downloads the model)...")

    store = FAISS.from_documents(chunks, rag.get_embeddings())
    store.save_local(str(rag.INDEX_DIR))
    print(f"Saved index to {rag.INDEX_DIR}")

    # quick sanity check
    hit = store.similarity_search("fire safety", k=1)[0]
    print("\nSanity check, top hit for 'fire safety':")
    print(f"  {hit.metadata['source_name']} p.{hit.metadata['page_no']}: {hit.page_content[:150]!r}")


if __name__ == "__main__":
    main()
