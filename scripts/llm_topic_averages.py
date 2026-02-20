import pandas as pd
from pathlib import Path

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- PATHS --------
LLM_FILE = BASE_DIR / "outputs" / "llm_detm_nyt_scores.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "llm_topic_averages_nyt.csv"

# -------- LOAD DATA --------
df = pd.read_csv(LLM_FILE)

# -------- AGGREGATE PER TOPIC --------
llm_avg = (
    df.groupby("topic_id")[["llm_temporal_coherence", "llm_temporal_smoothness"]]
    .mean()
    .reset_index()
)

llm_avg.rename(
    columns={
        "llm_temporal_coherence": "llm_coherence",
        "llm_temporal_smoothness": "llm_smoothness",
    },
    inplace=True,
)

# -------- SAVE --------
llm_avg.to_csv(OUTPUT_FILE, index=False)

print("LLM topic-level averages saved to:", OUTPUT_FILE)
print(llm_avg.head())

