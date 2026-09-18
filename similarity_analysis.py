"""
Document Similarity Analysis using the Vector Space Model (VSM)
=================================================================

This script:
1. Loads a set of text documents from the 'documents/' folder.
2. Preprocesses the text (lowercasing, punctuation removal, stopword removal).
3. Converts each document into a TF-IDF vector (the Vector Space Model).
4. Computes pairwise cosine similarity between every pair of documents.
5. Saves the results as a CSV file and a heatmap visualization.
6. Prints a ranked list of the most similar and most different document pairs.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS_DIR = "documents"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because
been before being below between both but by can't cannot could couldn't did
didn't do does doesn't doing don't down during each few for from further had
hadn't has hasn't have haven't having he he'd he'll he's her here here's hers
herself him himself his how how's i i'd i'll i'm i've if in into is isn't it
it's its itself let's me more most mustn't my myself no nor not of off on once
only or other ought our ours ourselves out over own same shan't she she'd
she'll she's should shouldn't so some such than that that's the their theirs
them themselves then there there's these they they'd they'll they're they've
this those through to too under until up very was wasn't we we'd we'll we're
we've were weren't what what's when when's where where's which while who
who's whom why why's with won't would wouldn't you you'd you'll you're you've
your yours yourself yourselves
""".split())


def load_documents(docs_dir):
    documents = {}
    for filename in sorted(os.listdir(docs_dir)):
        if filename.lower().endswith(".txt"):
            path = os.path.join(docs_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents[filename] = f.read()
    return documents


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return " ".join(tokens)


def build_tfidf_matrix(cleaned_texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
    return tfidf_matrix, vectorizer


def compute_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)


def main():
    print("Step 1: Loading documents...")
    documents = load_documents(DOCS_DIR)
    filenames = list(documents.keys())
    print(f"Loaded {len(filenames)} documents:")
    for name in filenames:
        print(f"  - {name}")

    print("\nStep 2: Preprocessing text...")
    cleaned_texts = [preprocess(documents[name]) for name in filenames]

    print("\nStep 3: Building TF-IDF vector space model...")
    tfidf_matrix, vectorizer = build_tfidf_matrix(cleaned_texts)
    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())} unique terms")
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape} (documents x terms)")

    print("\nStep 4: Computing cosine similarity between all document pairs...")
    sim_matrix = compute_similarity(tfidf_matrix)

    short_labels = [f"Doc{i+1}" for i in range(len(filenames))]
    sim_df = pd.DataFrame(sim_matrix, index=short_labels, columns=short_labels)

    print("\nCosine Similarity Matrix:")
    print(sim_df.round(3))

    csv_path = os.path.join(RESULTS_DIR, "similarity_matrix.csv")
    sim_df.round(4).to_csv(csv_path)
    print(f"\nSaved similarity matrix to {csv_path}")

    legend_path = os.path.join(RESULTS_DIR, "document_legend.csv")
    pd.DataFrame({"Label": short_labels, "Filename": filenames}).to_csv(legend_path, index=False)

    plt.figure(figsize=(9, 7))
    sns.heatmap(sim_df, annot=True, fmt=".2f", cmap="YlGnBu", vmin=0, vmax=1,
                square=True, cbar_kws={"label": "Cosine Similarity"})
    plt.title("Document Similarity Matrix (TF-IDF + Cosine Similarity)", fontsize=13)
    plt.tight_layout()
    heatmap_path = os.path.join(RESULTS_DIR, "similarity_heatmap.png")
    plt.savefig(heatmap_path, dpi=150)
    plt.close()
    print(f"Saved heatmap to {heatmap_path}")

    print("\nStep 5: Ranking document pairs by similarity...")
    pairs = []
    n = len(short_labels)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((short_labels[i], short_labels[j],
                          filenames[i], filenames[j], sim_matrix[i, j]))
    pairs_df = pd.DataFrame(pairs, columns=["Doc A", "Doc B", "File A", "File B", "Similarity"])
    pairs_df = pairs_df.sort_values("Similarity", ascending=False).reset_index(drop=True)

    pairs_csv = os.path.join(RESULTS_DIR, "ranked_pairs.csv")
    pairs_df.round(4).to_csv(pairs_csv, index=False)

    print("\nTop 5 most similar document pairs:")
    print(pairs_df.head(5)[["Doc A", "Doc B", "Similarity"]].to_string(index=False))

    print("\nTop 5 least similar document pairs:")
    print(pairs_df.tail(5)[["Doc A", "Doc B", "Similarity"]].to_string(index=False))

    print("\nDone. All results saved in the 'results/' folder.")


if __name__ == "__main__":
    main()
