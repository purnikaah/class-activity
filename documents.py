"""
documents.py
------------
Handles the document collection: loading existing documents from the
'corpus' folder and adding new ones at runtime.

Each document is a plain .txt file. The "document ID" is simply the
filename (e.g. "doc1.txt"), which makes the system easy to inspect and
debug by hand.
"""

import os

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "corpus")


def ensure_corpus_dir():
    """Create the corpus folder if it doesn't exist yet."""
    os.makedirs(CORPUS_DIR, exist_ok=True)


def load_documents():
    """
    Load all documents from the corpus folder.

    Returns:
        dict: {doc_id (str): text (str)}
    """
    ensure_corpus_dir()
    documents = {}
    for filename in sorted(os.listdir(CORPUS_DIR)):
        if filename.endswith(".txt"):
            path = os.path.join(CORPUS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents[filename] = f.read()
    return documents


def add_document(doc_id, text):
    """
    Add a new document to the collection on disk.

    Args:
        doc_id (str): filename to save as, e.g. "doc9.txt"
        text (str): the document's content

    Returns:
        str: the doc_id actually used (adjusted if it already existed)
    """
    ensure_corpus_dir()

    if not doc_id.endswith(".txt"):
        doc_id += ".txt"

    # Avoid silently overwriting an existing document.
    base, ext = os.path.splitext(doc_id)
    counter = 1
    final_id = doc_id
    while os.path.exists(os.path.join(CORPUS_DIR, final_id)):
        final_id = f"{base}_{counter}{ext}"
        counter += 1

    path = os.path.join(CORPUS_DIR, final_id)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return final_id
