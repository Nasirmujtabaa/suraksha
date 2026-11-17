"""Test the bot on questions.csv and write results.csv (W11-12 field test).
Usage: python evaluate.py
'expect' = a keyword that must appear in the answer, or NOT_FOUND if the bot must refuse.
Edit questions.csv with 30 real questions and check expected keywords against your manuals.
"""
import csv

import rag

store, llm = rag.load_index(), rag.get_llm()
rows, passed = [], 0
with open("questions.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        res = rag.answer_question(r["question"], "en", store, llm)
        if r["expect"] == "NOT_FOUND":
            ok = not res["found"]
        else:
            ok = res["found"] and r["expect"].lower() in res["answer"].lower()
        passed += ok
        top = res["sources"][0] if res["sources"] else {}
        rows.append({"question": r["question"], "expect": r["expect"], "pass": ok,
                     "answer": res["answer"] or "NOT_FOUND",
                     "top_source": f'{top.get("name","")} p.{top.get("page","")}'})
        print(("PASS" if ok else "FAIL"), "-", r["question"])

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"\n{passed}/{len(rows)} passed. Details in results.csv (also verify answers manually!)")
