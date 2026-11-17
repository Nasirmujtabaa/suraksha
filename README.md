# Suraksha – RAG-Based Assistant

## Project Overview
Suraksha is a Retrieval-Augmented Generation (RAG) based application designed to provide answers using information retrieved from a document knowledge base.

## Features
- Document-based question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- FAISS-based document retrieval
- Interactive Streamlit interface

## Technology Stack
- Python
- Streamlit
- Retrieval-Augmented Generation (RAG)
- FAISS
- [Add your actual embedding model and LLM here]

## Project Structure
- `app.py` – Main application
- `rag.py` – RAG implementation
- `build_index.py` – Vector index generation
- `evaluate.py` – Evaluation script
- `data/` – Source documents
- `faiss_index/` – Vector database
- `questions.csv` – Evaluation questions
- `results.csv` – Evaluation results

## Installation and Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Run the application:

   `python -m streamlit run app.py`

## Evaluation
The project includes an evaluation script and a set of sample questions. Refer to `evaluate.py` and `questions.csv`.

## Author
[Your Name]

## License
For academic and educational purposes.
