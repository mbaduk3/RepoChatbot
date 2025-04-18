import re

def tokenize_and_normalize(text):
    STOPWORDS = {
        "def", "class", "if", "else", "elif", "return", "in", "for", "while",
        "import", "from", "as", "with", "pass", "print", "and", "or", "not"
    }
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def summarize_file(query, parsed_files):
    tokens = tokenize_and_normalize(query)
    for file in parsed_files:
        if file.filename.strip(".py") in tokens:
            funcs = [f.name for f in file.functions]
            classes = [c.name for c in file.classes]
            return {
                "file": file.path,
                "functions": funcs,
                "classes": classes,
                "lines": file.lines
            }
    return f"No file found to summarize."


def rank_matches(token, inverted_index, symbol_table):
    matches = inverted_index.get(token.lower(), [])
    ranked = []
    for match in matches:
        score = 1
        file = match["file"]
        line = match["line"]
        sym = symbol_table.get(token)
        if sym and sym.file == file and sym.line == line:
            score = 3
        elif sym and sym.file == file:
            score = 2
        ranked.append({"file": file, "line": line, "score": score})
    ranked.sort(key=lambda x: (-x["score"], x["line"]))
    return ranked


def keyword_search(query, inverted_index):
    tokens = tokenize_and_normalize(query)
    results = []
    seen = set()
    for token in tokens:
        for entry in inverted_index.get(token, []):
            key = (entry["file"], entry["line"])
            if key not in seen:
                results.append(entry)
                seen.add(key)
    return results