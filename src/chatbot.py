import os
import json
from classify_query import classify_query_tfidf
from operations import rank_matches, summarize_file, keyword_search
from scan_filetree import scan_repo
from embed_common_queries import save_tfidf_vectors_to_file
from format_output import format_response
from extract_symbol import extract_symbol
from format_output import print_code_snippet
from res.common_queries import COMMON_QUERIES

EMBEDDINGS_PATH = "/res/common_query_embeddings.json"


def dispatch_query(query, embeddings, symbol_table, inverted_index, parsed_files):
    query_type = classify_query_tfidf(query, embeddings)
    symbol = extract_symbol(query, embeddings)
    print(f"Extracted symbol: {symbol}")

    if query_type == "definition":
        return symbol_table.get(symbol)
    elif query_type == "usage":
        return rank_matches(symbol, inverted_index, symbol_table)
    elif query_type == "library_usage":
        return inverted_index.get(symbol.lower(), [])
    elif query_type == "summary":
        return summarize_file(query, parsed_files)
    elif query_type == "generic_search":
        return keyword_search(query, inverted_index)
    else:
        return f"Query type '{query_type}' not yet implemented."


def run_chatbot(root_directory: str):
    # Scan and parse file tree 
    parsed_files, symbol_table, inverted_index = scan_repo(root_directory, ".py")

    # Build common query embeddings if needed
    embedding_path = os.path.dirname(os.path.abspath(__file__)) + EMBEDDINGS_PATH
    if not os.path.exists(embedding_path):
        save_tfidf_vectors_to_file(COMMON_QUERIES, embedding_path)
    
    # Load common query embeddings
    with open(embedding_path, 'r') as file:
        common_vector_embeddings = json.load(file)

    # Accept user input
    print("Ready! Ask questions about the repo (type 'exit' to quit).\n")
    while True:
        user_query = input("You: ")
        if user_query.strip().lower() in {"exit", "quit"}:
            break

        query_type = classify_query_tfidf(user_query, common_vector_embeddings)
        print("Classifying this query as: " + query_type)
        result = dispatch_query(user_query, common_vector_embeddings, symbol_table, inverted_index, parsed_files)
        response = format_response(query_type, result, parsed_files)
        if isinstance(response, tuple):
            formatted = response[0]
            snippet = response[1]
        else:
            formatted = response
            snippet = None
        print(f"Bot: {formatted}")
        if snippet:
            print_code_snippet(snippet)


if __name__ == "__main__":
    run_chatbot(".")