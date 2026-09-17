# Mini Boolean Information Retrieval System

A small Information Retrieval (IR) system built for a course assignment.
It indexes a collection of text documents and supports Boolean search
(`AND`, `OR`, `NOT`, parentheses) over them.

See [REPORT.md](REPORT.md) for the full write-up of design decisions.

## Features

- Add documents to the collection at runtime
- Build a dictionary (vocabulary) from the collection
- Build an inverted index (term → document IDs)
- Boolean retrieval: `AND`, `OR`, `NOT`, and parenthesized expressions

## Requirements

- Python 3.7+
- No external dependencies (standard library only)

## Usage

```bash
git clone <your-repo-url>
cd ir_system
python3 main.py
```

You'll see a menu:

```
1. View document collection
2. Add a new document
3. View the dictionary
4. View the inverted index
5. Run a Boolean search
6. Exit
```

### Example query

```
Enter a Boolean query (e.g. 'cat AND dog', 'NOT bird'): (cat OR dog) AND NOT bird
2 document(s) matched: ['doc1.txt', 'doc2.txt']
```

## Project structure

```
ir_system/
├── corpus/              # the document collection (.txt files)
├── documents.py         # load_documents(), add_document()
├── index_builder.py     # tokenize(), build_dictionary(), build_inverted_index()
├── boolean_retrieval.py # Boolean query parser + evaluator
├── main.py              # CLI entry point
└── REPORT.md            # assignment report
```
