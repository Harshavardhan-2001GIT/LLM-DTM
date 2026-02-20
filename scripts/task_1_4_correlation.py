import pandas as pd
from scipy.stats import spearmanr
from pathlib import Path

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- PATHS --------
HUMAN_FILE = BASE_DIR / "outputs" / "human_topic_averages_nyt.csv"
LLM_FILE = BASE_DIR / "outputs" / "llm_topic_averages_nyt.csv"

# -------- LOAD DATA --------
human_df = pd.read_csv(HUMAN_FILE)
llm_df = pd.read_csv(LLM_FILE)

# -------- MERGE ON TOPIC ID --------
merged = pd.merge(human_df, llm_df, on="topic_id", how="inner")

print("Merged data preview:\n")
print(merged.head())

# -------- SPEARMAN CORRELATIONS --------
corr_coh, p_coh = spearmanr(
    merged["human_word_relatedness"],
    merged["llm_coherence"]
)

corr_smooth, p_smooth = spearmanr(
    merged["human_smoothness"],
    merged["llm_smoothness"]
)

print("\n=== Task 1.4 Results ===")
print(f"Spearman correlation (Human coherence vs LLM coherence): {corr_coh:.3f} (p={p_coh:.4f})")
print(f"Spearman correlation (Human smoothness vs LLM smoothness): {corr_smooth:.3f} (p={p_smooth:.4f})")

