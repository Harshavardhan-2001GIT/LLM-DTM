from pathlib import Path
import subprocess
import random
import pandas as pd

# -------- PATHS --------
DATA_DIR = Path(r"D:\LLM Evaluation for DTM\prolific\prolific\DETM\nyt")
PROMPT_PATH = Path("prompts/intrusion_eval.txt")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "llm_intrusion_detm_nyt.csv"

# -------- PARAMETERS --------
YEAR = 1988
TOPICS = list(range(10))        # topics 0–9
INTRUSIONS_PER_TOPIC = 5

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

rows = []

for topic_id in TOPICS:
    print(f"Processing topic {topic_id}...")
    topic_words = get_topic_words(YEAR, topic_id)

    for _ in range(INTRUSIONS_PER_TOPIC):
        intruder_topic = random.choice([t for t in TOPICS if t != topic_id])
        intruder_word = get_topic_words(YEAR, intruder_topic)[0]

        words = topic_words[:5] + [intruder_word]
        random.shuffle(words)

        template = PROMPT_PATH.read_text(encoding="utf-8")
        prompt = template.format(words=", ".join(words))

        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="ignore",
            capture_output=True
        )

        llm_answer = result.stdout.strip().split()[0].lower()
        correct = int(llm_answer == intruder_word.lower())

        rows.append({
            "dataset": "NYT",
            "model": "DETM",
            "topic_id": topic_id,
            "year": YEAR,
            "intruder_word": intruder_word,
            "llm_choice": llm_answer,
            "correct": correct
        })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ DONE")
print(f"Saved results to: {OUTPUT_FILE}")
