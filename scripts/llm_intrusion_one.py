from pathlib import Path
import subprocess
import random

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- PATHS --------
DATA_DIR = BASE_DIR / "data" / "DETM" / "nyt"
PROMPT_PATH = BASE_DIR / "prompts" / "intrusion_eval.txt"

# -------- PARAMETERS --------
year = 1988
topic_id = 0              # main topic
intruder_topic_id = 1     # source of intruder word

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

# -------- GET WORDS --------
topic_words = get_topic_words(year, topic_id)[:5]
intruder_word = get_topic_words(year, intruder_topic_id)[0]

all_words = topic_words + [intruder_word]
random.shuffle(all_words)

# -------- BUILD PROMPT --------
template = PROMPT_PATH.read_text(encoding="utf-8")
prompt = template.format(words=", ".join(all_words))

print("\nPROMPT SENT TO LLM:\n")
print(prompt)
print("\n--- LLM RESPONSE ---\n")

# -------- CALL LLM --------
result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    encoding="utf-8",
    errors="ignore",
    capture_output=True
)

print(result.stdout.strip())
print("\nGROUND TRUTH INTRUDER:", intruder_word)
