from pathlib import Path

# Base directory = project root (LLM-DTM)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory inside repo
DATA_DIR = BASE_DIR / "data" / "DETM" / "nyt"

topic_id = 0
years = [1987, 1992, 1997, 2002, 2007]

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

print(f"\nTopic {topic_id} evolution:\n")

for y in years:
    words = get_topic_words(y, topic_id)
    print(f"{y}: {', '.join(words[:10])}")

