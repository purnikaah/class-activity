"""
main.py
-------
Command-line entry point for the mini IR system.

Menu options:
    1. View document collection
    2. Add a new document
    3. View the dictionary (vocabulary)
    4. View the inverted index
    5. Run a Boolean search
    6. Exit
"""

import documents
import index_builder
from boolean_retrieval import BooleanRetrieval


def print_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def show_documents(docs):
    print_header("DOCUMENT COLLECTION")
    for doc_id, text in docs.items():
        print(f"[{doc_id}] {text.strip()}")


def show_dictionary(vocab):
    print_header(f"DICTIONARY ({len(vocab)} terms)")
    print(", ".join(vocab))


def show_inverted_index(index):
    print_header("INVERTED INDEX")
    for term, postings in index.items():
        print(f"{term:15} -> {postings}")


def run_search(retrieval_engine):
    query = input("\nEnter a Boolean query (e.g. 'cat AND dog', 'NOT bird'): ")
    try:
        results = retrieval_engine.search(query)
        if results:
            print(f"\n{len(results)} document(s) matched: {results}")
        else:
            print("\nNo documents matched this query.")
    except ValueError as e:
        print(f"\nQuery error: {e}")


def main():
    docs = documents.load_documents()

    while True:
        vocab = index_builder.build_dictionary(docs)
        inv_index = index_builder.build_inverted_index(docs)
        retrieval_engine = BooleanRetrieval(inv_index, docs.keys())

        print_header("MINI IR SYSTEM")
        print(f"Documents loaded: {len(docs)}")
        print("1. View document collection")
        print("2. Add a new document")
        print("3. View the dictionary")
        print("4. View the inverted index")
        print("5. Run a Boolean search")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_documents(docs)
        elif choice == "2":
            doc_id = input("New document filename (e.g. doc9): ").strip()
            text = input("Document text: ").strip()
            final_id = documents.add_document(doc_id, text)
            docs = documents.load_documents()  # reload + re-index next loop
            print(f"Added as '{final_id}'. Index has been rebuilt.")
        elif choice == "3":
            show_dictionary(vocab)
        elif choice == "4":
            show_inverted_index(inv_index)
        elif choice == "5":
            run_search(retrieval_engine)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
