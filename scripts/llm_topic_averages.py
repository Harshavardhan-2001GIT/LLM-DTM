import pandas as pd

# -------- PATH --------
LLM_FILE = r"D:\LLM Evaluation for DTM\outputs\llm_detm_nyt_scores.csv"

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
llm_avg.to_csv("outputs/llm_topic_averages_nyt.csv", index=False)

print("✅ LLM topic-level averages saved to outputs/llm_topic_averages_nyt.csv")
print(llm_avg.head())
