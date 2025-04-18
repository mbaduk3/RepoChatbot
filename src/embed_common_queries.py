import json
import math
import os
from collections import defaultdict
from pathlib import Path
from vector_utils import tokenize, build_tf
from res.common_queries import COMMON_QUERIES


def compute_idf(documents):
    """Compute inverse document frequency (IDF) for each word in the corpus."""
    df = defaultdict(int)
    total_docs = len(documents)

    for tokens in documents:
        for token in set(tokens):  # unique terms only
            df[token] += 1

    idf = {token: math.log(total_docs / df[token]) for token in df}
    return idf


def save_tfidf_vectors_to_file(common_queries, output_path):
    """
    Given a dictionary of labeled example phrases, compute TF-IDF vectors
    and save them to a JSON file at the given output path.

    Parameters:
    - common_queries: dict[label -> list of phrases]
    - output_path: string or Path where JSON file will be saved
    """
    labels = []
    documents = []

    # Prepare list of documents and labels
    for label, examples in common_queries.items():
        for entry in examples:
            phrase = entry["phrase"]
            symbol = entry.get("symbol", "")
            tokens = tokenize(phrase)
            documents.append(tokens)
            labels.append((label, phrase, symbol))

    idf = compute_idf(documents)

    tfidf_vectors = []
    for tokens, (label, phrase, symbol) in zip(documents, labels):
        tf = build_tf(tokens)
        tfidf = {word: tf[word] * idf[word] for word in tf}
        tfidf_vectors.append({
            "label": label,
            "phrase": phrase,
            "symbol": symbol,
            "vector": tfidf
        })

    output_file = Path(output_path)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(tfidf_vectors, f, indent=2)

    return output_file

if __name__ == "__main__":
    save_tfidf_vectors_to_file(COMMON_QUERIES, os.path.dirname(__file__) + "/res/common_query_embeddings.json")