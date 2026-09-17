"""
index_builder.py
-----------------
Builds the two core data structures of the IR system:

1. The DICTIONARY  -> the sorted set of all unique terms (the vocabulary).
2. The INVERTED INDEX -> a mapping from each term to the sorted list of
   document IDs that contain that term.

Tokenization rules (kept intentionally simple for this assignment):
    - Lowercase everything (so "Dog" and "dog" are treated as the same term)
    - Strip punctuation
    - Split on whitespace
    - No stemming/lemmatization and no stopword removal, so the index
      stays easy to trace by hand for the report.
"""

import re

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text):
    """Lowercase and split text into alphanumeric tokens."""
    return TOKEN_PATTERN.findall(text.lower())


def build_dictionary(documents):
    """
    Build the vocabulary (dictionary) from the document collection.

    Args:
        documents (dict): {doc_id: text}

    Returns:
        list: sorted list of unique terms
    """
    vocabulary = set()
    for text in documents.values():
        vocabulary.update(tokenize(text))
    return sorted(vocabulary)


def build_inverted_index(documents):
    """
    Build the inverted index from the document collection.

    Args:
        documents (dict): {doc_id: text}

    Returns:
        dict: {term: sorted list of doc_ids containing that term}
    """
    index = {}
    for doc_id, text in documents.items():
        terms = set(tokenize(text))  # set() -> record presence, not frequency
        for term in terms:
            index.setdefault(term, set()).add(doc_id)

    # Convert sets to sorted lists (postings lists) for stable, readable output
    return {term: sorted(doc_ids) for term, doc_ids in sorted(index.items())}
