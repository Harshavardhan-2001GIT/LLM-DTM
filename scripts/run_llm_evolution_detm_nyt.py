from pathlib import Path
import subprocess
import json
import re
import pandas as pd

# -------- PATHS --------
DATA_DIR = Path(r"D:\LLM Evaluation for DTM\prolific\prolific\DETM\nyt")
PROMPT_PATH = Path("prompts/evolution_eval.txt")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "llm_evolution_detm_nyt.csv"

# -------- PARAMETERS --------
TOPICS = list(range(10))  # topics 0–9
YEARS = [1987, 1992, 1997, 2002, 2007]

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

def extract_json(text):
    match = re.search(r"\{[\s\S]*?\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

rows = []

for topic_id in TOPICS:
    print(f"Processing topic {topic_id}...")

    timeline_lines = []
    for y in YEARS:
        words = get_topic_words(y, topic_id)
        timeline_lines.append(f"{y}: {', '.join(words[:10])}")

    timeline_text = "\n".join(timeline_lines)

    template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = template.format(timeline=timeline_text)

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )

    output = result.stdout + "\n" + result.stderr
    parsed = extract_json(output)

    if parsed is None:
        print(f"⚠️ No valid JSON for topic {topic_id}")
        continue

    rows.append({
        "dataset": "NYT",
        "model": "DETM",
        "topic_id": topic_id,
        "evolution_type": parsed.get("evolution_type"),
        "brief_explanation": parsed.get("brief_explanation")
    })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("\n DONE")
print(f"Saved results to: {OUTPUT_FILE}")

