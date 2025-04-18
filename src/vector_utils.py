import re
import math
from collections import Counter

def tokenize(text):
    """Tokenize and normalize a string into lowercase words."""
    return [w.lower() for w in re.findall(r'\b\w+\b', text)]

def build_tf(tokens):
    """Convert a list of tokens into a normalized term frequency (TF) vector."""
    tf = Counter(tokens)
    total = sum(tf.values())
    return {word: count / total for word, count in tf.items()}

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors (dicts)."""
    common = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[word] * vec2[word] for word in common)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0