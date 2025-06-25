#!/bin/bash

# === Step 1: Record from Microphone ===
echo "🎤 Recording your idea..."
python3 idea-recoder.py

# === Step 2: Transcribe using whisper.cpp ===
echo "📝 Transcribing audio..."
./whisper.cpp/build/bin/whisper-cli -m ./whisper.cpp/models/ggml-base.en.bin -f idea.wav -otxt

# === Step 3: Summarize and Save ===
echo "🧠 Summarizing and saving the idea..."
python3 save-summary.py

echo "✅ Done! Idea saved to ideas.json."
