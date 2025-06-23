import json
from datetime import datetime
import subprocess

# === Config ===
TRANSCRIPT_FILE = "idea.wav.txt"
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
LLAMA_CLI = "llama.cpp/build/bin/llama-cli"
SAVE_FILE = "ideas.json"

# === Load transcript ===
with open(TRANSCRIPT_FILE, "r") as f:
    raw_text = f.read().strip()

# === Run LLM summary ===
prompt = f"Summarize and describe this idea: {raw_text}"
result = subprocess.run(
    [LLAMA_CLI, "-m", MODEL_PATH, "-p", prompt],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)
summary = result.stdout.strip()

# === Build data entry ===
entry = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "raw": raw_text,
    "summary": summary
}

# === Save or append to ideas.json ===
try:
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

data.append(entry)

with open(SAVE_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Idea saved to ideas.json!")

