from pathlib import Path
import subprocess
import json
import re
import time
import pandas as pd

# ---------------- PATHS ----------------
DATA_DIR = Path(r"D:\LLM Evaluation for DTM\prolific\prolific\DLDA\neurips")
PROMPT_PATH = Path("prompts/temporal_eval.txt")

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "llm_dlda_neurips_scores.csv"


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "llm_detm_nyt_scores.csv"

# ---------------- PARAMETERS ----------------
NUM_TOPICS = 5
SLEEP_TIME = 0.2  # seconds between LLM calls

# ---------------- LOAD PROMPT ----------------
template = PROMPT_PATH.read_text(encoding="utf-8")

# ---------------- HELPERS ----------------
def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

def call_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )
    return result.stdout

def parse_json(output):
    match = re.search(r"\{[\s\S]*?\}", output)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

# ---------------- MAIN LOOP ----------------
rows = []

years = sorted(int(p.stem) for p in DATA_DIR.glob("*.txt"))

for topic_id in range(NUM_TOPICS):
    print(f"Processing topic {topic_id}...")
    for i in range(1, len(years) - 1):
        y_prev, y_curr, y_next = years[i-1], years[i], years[i+1]

        words_prev = get_topic_words(y_prev, topic_id)
        words_curr = get_topic_words(y_curr, topic_id)
        words_next = get_topic_words(y_next, topic_id)

        prompt = template.format(
            prev_words=", ".join(words_prev[:10]),
            curr_words=", ".join(words_curr[:10]),
            next_words=", ".join(words_next[:10]),
        )

        output = call_llm(prompt)
        parsed = parse_json(output)

        if parsed is None:
            print(f"⚠️ JSON failed for topic {topic_id}, year {y_curr}")
            continue

        rows.append({
            "dataset": "NeurIPS",
            "model": "DLDA",


            "topic_id": topic_id,
            "year": y_curr,
            "llm_temporal_coherence": parsed.get("temporal_coherence"),
            "llm_temporal_smoothness": parsed.get("temporal_smoothness"),
        })

        time.sleep(SLEEP_TIME)

# ---------------- SAVE ----------------
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ DONE")
print(f"Saved results to: {OUTPUT_FILE}")
