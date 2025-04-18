# Repo Chatbot

A Python-powered assistant for exploring codebases using natural language. It classifies questions, extracts relevant symbols, and returns contextual answers with code snippets.

## Features
- Query classification via TF-IDF + cosine similarity
- Symbol extraction using pattern matching
- Code usage/definition lookup with snippet display
- Rich terminal formatting using `rich`

## Usage
```bash
python chatbot_cli.py
```

Ask questions like:
- "Where is `vector_utils` used?"
- "Define `tokenize_and_normalize`"
- "Summarize `chatbot.py`"


## Requirements
```bash
pip install -r requirements.txt 
```
