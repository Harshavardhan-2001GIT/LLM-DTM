# LLM-Based Evaluation of Dynamic Topic Models (DTM)

The goal is to compare Large Language Model (LLM) judgments with human evaluation scores.

Current Implementation

Dataset:
- DETM – NYT (50 topics across years)

Tasks implemented:

Task 1.1 – Temporal Coherence & Smoothness
- The LLM evaluates:
  - Word relatedness at time *t*
  - Smoothness of transition from *t-1 → t → t+1*
- Output stored as CSV

 Task 1.2 – Intrusion Detection
- One intruder word is inserted into topic words
- LLM identifies the word that does not belong

Task 1.3 – Topic Evolution Classification
- The LLM classifies long-term topic evolution as:
  - Smooth and coherent evolution
  - Gradual semantic drift
  - Abrupt topic shift
  - Largely incoherent evolution

Task 1.4 – Human vs LLM Correlation
- Topic-level averages are computed
- Spearman correlation is calculated between:
  - Human word relatedness vs LLM coherence
  - Human smoothness vs LLM smoothness

---
 Model Setup

The experiments use a local LLM via **Ollama**.


