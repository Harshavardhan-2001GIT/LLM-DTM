from pathlib import Path
import subprocess

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- PATHS --------
DATA_DIR = BASE_DIR / "data" / "DETM" / "nyt"
PROMPT_PATH = BASE_DIR / "prompts" / "temporal_eval.txt"

# -------- TOPIC + YEARS --------
topic_id = 0
years = [1987, 1988, 1989]

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

words_prev = get_topic_words(years[0], topic_id)
words_curr = get_topic_words(years[1], topic_id)
words_next = get_topic_words(years[2], topic_id)

# -------- BUILD PROMPT --------
template = PROMPT_PATH.read_text(encoding="utf-8")

prompt = template.format(
    prev_words=", ".join(words_prev[:10]),
    curr_words=", ".join(words_curr[:10]),
    next_words=", ".join(words_next[:10]),
)

print("PROMPT SENT TO LLM:\n")
print(prompt)
print("\n--- LLM RESPONSE ---\n")

# -------- CALL OLLAMA --------
result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    encoding="utf-8",
    errors="ignore",
    capture_output=True
)

print(result.stdout)


