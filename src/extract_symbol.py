import re
from vector_utils import tokenize, build_tf, cosine_similarity

def extract_symbol_by_pattern_match(query: str, embeddings) -> str:
    """
    Matches a query to a common example, then identifies the most likely symbol
    by finding the corresponding token in the user query.
    """
    query_tokens = tokenize(query)
    query_vec = build_tf(query_tokens)

    best_score = 0
    best_example = None

    for ex in embeddings:
        sim = cosine_similarity(query_vec, ex["vector"])
        if sim > best_score:
            best_score = sim
            best_example = ex

    if not best_example:
        return ""

    example_tokens = tokenize(best_example["phrase"])
    symbol_token = best_example["symbol"].lower()

    # Find the position of the symbol in the example phrase
    try:
        symbol_index = example_tokens.index(symbol_token)
    except ValueError:
        symbol_index = -1

    # Try to return token from user query at same position
    if 0 <= symbol_index < len(query_tokens):
        return query_tokens[symbol_index]

    return ""


def extract_symbol(query: str, embeddings) -> str:
    # 1. Try to find symbol in backticks
    match = re.search(r"`([^`]+)`", query)
    if match:
        return match.group(1)
    
    # 2. Try to use sematic similarity
    return extract_symbol_by_pattern_match(query, embeddings)