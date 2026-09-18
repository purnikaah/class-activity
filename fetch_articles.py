import os
import requests

DOCS_DIR = "documents"
os.makedirs(DOCS_DIR, exist_ok=True)

TOPICS = [
    "Artificial_intelligence",
    "Machine_learning",
    "Climate_change",
    "Renewable_energy",
    "Quantum_computing",
    "Space_exploration",
    "Blockchain",
    "CRISPR_gene_editing",
]

API_URL = "https://en.wikipedia.org/w/api.php"


def fetch_article_text(title):
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
    }
    headers = {"User-Agent": "similarity-assignment-script/1.0"}
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "")


def main():
    for title in TOPICS:
        print(f"Fetching: {title} ...")
        try:
            text = fetch_article_text(title)
        except Exception as e:
            print(f"  Failed to fetch {title}: {e}")
            continue
        if not text.strip():
            print(f"  No content returned for {title}, skipping.")
            continue
        filename = f"{title.lower()}.txt"
        path = os.path.join(DOCS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  Saved {path} ({len(text.split())} words)")
    print("\nDone. Check the 'documents/' folder.")


if __name__ == "__main__":
    main()
