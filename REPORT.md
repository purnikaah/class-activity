# Mini Information Retrieval System — Report

## 1. Overview

This project implements a small Boolean Information Retrieval (IR) system
over a collection of 8 short text documents. It supports:

- Adding new documents to the collection at runtime
- Building a **dictionary** (vocabulary) from the collection
- Building an **inverted index** mapping terms to the documents they appear in
- **Boolean retrieval** using `AND`, `OR`, `NOT`, and parentheses

The system is implemented in Python 3 with no external dependencies, split
into four modules: `documents.py`, `index_builder.py`,
`boolean_retrieval.py`, and `main.py` (the CLI).

## 2. Document Collection

Eight short documents (`corpus/doc1.txt` – `corpus/doc8.txt`) were written
around overlapping themes (animals, and information retrieval concepts) so
that Boolean queries return interesting, non-trivial results. Each document
is a plain `.txt` file, and the filename doubles as its document ID — this
keeps the system transparent and easy to inspect by hand.

| Doc ID | Content summary |
|---|---|
| doc1.txt | Cat and dog in a yard |
| doc2.txt | Dogs as loyal pets |
| doc3.txt | Cats are independent |
| doc4.txt | IR systems help users find documents |
| doc5.txt | Search engines and inverted indexes |
| doc6.txt | Birds fly, cats/dogs don't |
| doc7.txt | Machine learning for ranking search results |
| doc8.txt | Dog chases a bird |

New documents can be added through the CLI (option 2), which writes a new
`.txt` file into `corpus/` and triggers a full re-index.

## 3. Tokenization

Tokenization rules were kept deliberately simple so the resulting index is
easy to trace by hand for grading/demonstration purposes:

- All text is lowercased (so `Dog` and `dog` are the same term)
- Tokens are matched with the regex `[a-zA-Z0-9]+`, which strips punctuation
- No stopword removal and no stemming

**Design tradeoff:** A production IR system would typically remove stopwords
(`the`, `a`, `is`...) and apply stemming (`dogs` → `dog`) to shrink the index
and improve recall. I chose not to, so that the dictionary and inverted
index stay simple and directly traceable back to the original text — useful
for a learning exercise and for verifying correctness in the report.

## 4. Dictionary

The dictionary is the sorted set of all unique terms across the entire
collection. It is rebuilt from scratch each time the system starts (or after
a new document is added), via `index_builder.build_dictionary()`.

Example (truncated):
```
a, across, all, an, and, animals, are, as, at, away, be, bird, birds, ...
```

## 5. Inverted Index

The inverted index maps each term to a **postings list**: the sorted list of
document IDs in which that term appears. Only presence is recorded (not term
frequency or position), since this assignment implements Boolean retrieval,
not ranked retrieval.

Example entries:
```
cat   -> ['doc1.txt']
dog   -> ['doc1.txt', 'doc2.txt', 'doc8.txt']
bird  -> ['doc6.txt', 'doc8.txt']
```

**Data structure choice:** the index is built with Python sets internally
(for fast union/intersection during construction) and converted to sorted
lists for the final structure, so the output is deterministic and readable.

## 6. Boolean Retrieval

Boolean queries support `AND`, `OR`, `NOT`, and parentheses, e.g.:

```
cat AND dog
cat OR bird
NOT cat
(cat OR dog) AND NOT bird
```

**Implementation approach:** rather than using Python's `eval()` (unsafe and
hard to control for a custom grammar), queries are evaluated with a small
hand-written **recursive-descent parser**:

- `NOT` binds tightest, then `AND`, then `OR` — the standard IR convention
- `AND` is implemented as set intersection (`&`)
- `OR` is implemented as set union (`|`)
- `NOT` is implemented as set difference against the universe of all
  document IDs (`all_docs - operand`)

This means `NOT` requires knowing the full set of documents in the
collection, which the retrieval engine is given at construction time.

### Example results (from the current 8-document collection)

| Query | Result |
|---|---|
| `cat AND dog` | `['doc1.txt']` |
| `cat OR bird` | `['doc1.txt', 'doc8.txt']` |
| `NOT cat` | all docs except doc1.txt |
| `(cat OR dog) AND NOT bird` | `['doc1.txt', 'doc2.txt']` |

## 7. Program Structure

```
ir_system/
├── corpus/              # the document collection (.txt files)
├── documents.py         # load_documents(), add_document()
├── index_builder.py     # tokenize(), build_dictionary(), build_inverted_index()
├── boolean_retrieval.py # BooleanRetrieval class (parser + evaluator)
├── main.py              # CLI menu tying it all together
└── REPORT.md            # this report
```

## 8. Screenshots

*(Insert screenshots here of: (1) the CLI menu, (2) the dictionary printed,
(3) the inverted index printed, (4) two or three example Boolean queries
and their results, and (5) adding a new document and seeing the index
update.)*

## 9. How to Run

```bash
cd ir_system
python3 main.py
```

Then use the on-screen menu to view the collection, dictionary, inverted
index, or run a Boolean search.

## 10. Possible Extensions

- Stopword removal and stemming to shrink the index
- Ranked retrieval (TF-IDF / cosine similarity) instead of pure Boolean
- Phrase queries using positional indexes
- A simple web UI instead of a CLI
