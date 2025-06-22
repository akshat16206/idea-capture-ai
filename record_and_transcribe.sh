#!/bin/bash

echo " Recording idea..."
python3 idea_recorder.py

echo " Transcribing using whisper.cpp..."
./whisper.cpp/build/bin/whisper-cli -m ./whisper.cpp/models/ggml-base.en.bin -f idea.wav -otxt

echo "Transcription saved to idea.wav.txt"
