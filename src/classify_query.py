from vector_utils import tokenize, build_tf, cosine_similarity


def classify_query_tfidf(user_query, vector_embeddings) -> str:
    """
    Classify a user query based on cosine similarity to precomputed TF-IDF examples.

    Parameters:
    - user_query: str, the natural language query
    - vector_embeddings: str or Path, path to the saved JSON vector file

    Returns:
    - best_label: the predicted label (e.g., "usage", "summary")
    """

    # Tokenize and compute TF vector for the user query
    tokens = tokenize(user_query)
    query_tf = build_tf(tokens)

    # Compute cosine similarity to each example
    best_score = 0
    best_label = "generic_search"  # fallback
    for embedding in vector_embeddings:
        score = cosine_similarity(query_tf, embedding["vector"])
        if score > best_score:
            best_score = score
            best_label = embedding["label"]

    return best_label
