"""See what the search finds. Usage: python debug.py fire safety"""
import sys
from collections import Counter

import rag

store = rag.load_index()
docs = list(store.docstore._dict.values())
print(f"Index has {len(docs)} chunks from these files:")
for name, n in Counter(d.metadata.get("source_name") for d in docs).items():
    print(f"  {name}: {n} chunks")

q = " ".join(sys.argv[1:]) or "fire safety"
print(f"\nTop results for: {q!r}\n")
for d, score in store.similarity_search_with_score(q, k=5):
    print(f"[{score:.2f}] {d.metadata.get('source_name')} p.{d.metadata.get('page_no')}")
    print("   ", d.page_content[:250].replace("\n", " "), "\n")
