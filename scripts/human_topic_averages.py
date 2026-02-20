import pandas as pd
from pathlib import Path

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- PATHS --------
HUMAN_FILE = BASE_DIR / "data" / "survey_results" / "Dynamic Topic Evaluation (50) - NYT (Responses) - Form Responses 1.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "human_topic_averages_nyt.csv"

# -------- LOAD DATA --------
df = pd.read_csv(HUMAN_FILE)

# -------- FIND HUMAN RATING COLUMNS --------
word_cols = [c for c in df.columns if "Word relat" in c]
smooth_cols = [c for c in df.columns if "Smooth tra" in c]

print(f"Found {len(word_cols)} word-relatedness columns")
print(f"Found {len(smooth_cols)} smoothness columns")

human_rows = []

num_topics = min(len(word_cols), len(smooth_cols))

for topic_id in range(num_topics):
    word_scores = pd.to_numeric(df[word_cols[topic_id]], errors="coerce").dropna()
    smooth_scores = pd.to_numeric(df[smooth_cols[topic_id]], errors="coerce").dropna()

    human_rows.append({
        "topic_id": topic_id,
        "human_word_relatedness": word_scores.mean(),
        "human_smoothness": smooth_scores.mean()
    })

human_df = pd.DataFrame(human_rows)

# -------- SAVE --------
human_df.to_csv(OUTPUT_FILE, index=False)

print("Human topic-level averages saved to:", OUTPUT_FILE)
print(human_df.head())

