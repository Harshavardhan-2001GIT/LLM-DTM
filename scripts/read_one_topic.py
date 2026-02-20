from pathlib import Path

# -------- BASE DIRECTORY --------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------- DATA PATH --------
DATA_DIR = BASE_DIR / "data" / "DETM" / "nyt"

topic_id = 0
years = [1987, 1988, 1989]

def get_topic_words(year, topic_id):
    file_path = DATA_DIR / f"{year}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[topic_id].strip().split()

for y in years:
    words = get_topic_words(y, topic_id)
    print(f"{y}: {words[:10]}")


