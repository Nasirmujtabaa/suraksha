# Suraksha-RAG: Industrial Safety Assistant (India)

Shop-floor safety chatbot. Answers ONLY from your safety manuals, with source + page,
in English / Hindi / Kannada, with big buttons and voice search.

## 1. Setup (laptop)
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Get a free API key at https://console.groq.com and create `.streamlit/secrets.toml`
(copy from `secrets.toml.example`).

## 2. Add manuals (text-based PDFs) into `data/`
- Factories Act 1948: https://www.indiacode.nic.in (search "Factories Act, 1948")
- DGFASLI manuals: https://dgfasli.gov.in
- OSHA guidance: https://www.osha.gov/publications
Use clear file names (e.g. `Factories_Act_1948.pdf`): the name is shown as the citation.

## 3. Build the index, then run
```bash
python build_index.py          # creates faiss_index/
streamlit run app.py
```

## 4. Test (field-test week)
Edit `questions.csv` (30 real questions), run `python evaluate.py`, read `results.csv`,
and check every answer against the manual yourself.

## 5. Deploy (Streamlit Community Cloud)
1. Push the repo to GitHub, INCLUDING `faiss_index/` (not `secrets.toml`).
2. share.streamlit.io > New app > pick repo, main file `app.py`.
3. Advanced settings: Python 3.11; Secrets: paste `GROQ_API_KEY = "..."`.

## Safety notes
- Temperature is 0 and the prompt forces "NOT_FOUND" when the manuals don't answer.
- Always keep the disclaimer and source display. Never present this as a replacement for
  your factory's official procedures.
- Check which law is in force for your use case: India's Occupational Safety, Health and
  Working Conditions Code, 2020 is replacing the Factories Act 1948 (verify current status).

## If you get a 'model_not_found' error
Groq retires models often. Check https://console.groq.com/docs/models and set `GROQ_MODEL = "<new model id>"` in secrets.toml (no code change needed).
