from pathlib import Path
import subprocess

DATA_DIR = Path(r"D:\LLM Evaluation for DTM\prolific\prolific\DETM\nyt")
PROMPT_PATH = Path("prompts/evolution_eval.txt")

topic_id = 0
years = [1987, 1992, 1997, 2002, 2007]

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

timeline_lines = []

for y in years:
    words = get_topic_words(y, topic_id)
    timeline_lines.append(f"{y}: {', '.join(words[:10])}")

timeline_text = "\n".join(timeline_lines)

template = PROMPT_PATH.read_text(encoding="utf-8")
prompt = template.format(timeline=timeline_text)

print("\nPROMPT SENT TO LLM:\n")
print(prompt)
print("\n--- LLM RESPONSE ---\n")

result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    encoding="utf-8",
    errors="ignore",
    capture_output=True
)

print("\n--- RAW STDOUT ---\n")
print(result.stdout)

print("\n--- RAW STDERR ---\n")
print(result.stderr)

