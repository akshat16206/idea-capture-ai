import json
import sys

SEARCH_FILE = "ideas.json"

if len(sys.argv) < 2:
    print(" Please provide a search term.\nUsage: python3 search_ideas.py \"your keyword\"")
    exit()

query = sys.argv[1].lower()

try:
    with open(SEARCH_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("No ideas.json file found.")
    exit()
except json.JSONDecodeError:
    print(" ideas.json is corrupted.")
    exit()

results = []
for entry in data:
    if query in entry["summary"].lower() or query in entry["raw"].lower():
        results.append(entry)

if not results:
    print(" No matching ideas found.")
else:
    print(f"\n Found {len(results)} result{'s' if len(results) > 1 else ''}:\n")
    for idea in results:
        print(f"{idea['timestamp']}")
        print(f" Summary: {idea['summary']}\n")
