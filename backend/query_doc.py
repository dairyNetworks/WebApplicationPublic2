import json
from pathlib import Path

# --------------------------
# Utility function
# --------------------------
def load_json(file_path):
    """Load JSON from a file and return list of documents."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------
# Core query functions
# --------------------------
def find_top_documents_with_keyword_frequencies_or_json(json_file, keywords, top_n=5):
    keywords = [kw.replace(" ", "_") for kw in keywords]
    all_docs = load_json(json_file)

    # Filter documents: OR condition
    filtered_docs = [
        doc for doc in all_docs
        if any(doc.get("Term Document Matrix", {}).get(kw, 0) > 0 for kw in keywords)
    ]

    # Compute per-keyword counts and total frequency
    top_docs = []
    for doc in filtered_docs:
        keyword_counts = {kw: doc.get("Term Document Matrix", {}).get(kw, 0) for kw in keywords}
        total_frequency = sum(keyword_counts.values())

        if total_frequency > 0:
            top_docs.append({
                "File Name": doc.get("File Name", doc.get("file_name", "Unknown")),
                "keyword_counts": keyword_counts,
                "TotalFrequency": total_frequency,
                "count": 1
            })

    # Sort by TotalFrequency and limit
    top_docs = sorted(top_docs, key=lambda x: x["TotalFrequency"], reverse=True)[:top_n]

    # Print results
    for doc in top_docs:
        print(f"File Name: {doc['File Name']}")
        for kw, count in doc["keyword_counts"].items():
            print(f"  {kw}: {count}")
        print(f"  TotalFrequency: {doc['TotalFrequency']}\n")

    return top_docs

def find_top_documents_with_keyword_frequencies_and_json(json_file, keywords, top_n=5):
    keywords = [kw.replace(" ", "_") for kw in keywords]
    all_docs = load_json(json_file)

    filtered_docs = [
        doc for doc in all_docs
        if all(doc.get("Term Document Matrix", {}).get(kw, 0) > 0 for kw in keywords)
    ]

    top_docs = []
    for doc in filtered_docs:
        keyword_counts = {kw: doc.get("Term Document Matrix", {}).get(kw, 0) for kw in keywords}
        total_frequency = sum(keyword_counts.values())

        if total_frequency > 0:
            top_docs.append({
                "File Name": doc.get("File Name", doc.get("file_name", "Unknown")),
                "keyword_counts": keyword_counts,
                "TotalFrequency": total_frequency,
                "count": 1
            })

    top_docs = sorted(top_docs, key=lambda x: x["TotalFrequency"], reverse=True)[:top_n]

    for doc in top_docs:
        print(f"File Name: {doc['File Name']}")
        for kw, count in doc["keyword_counts"].items():
            print(f"  {kw}: {count}")
        print(f"  TotalFrequency: {doc['TotalFrequency']}\n")

    return top_docs


# --------------------------
# Combined function
# --------------------------
def function_call(keywords, json_file="static/data/complete_documents.json", top_n=5):
    keyword_list = []

    if "OR" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("OR")]
        top_documents = find_top_documents_with_keyword_frequencies_or_json(json_file, keyword_list, top_n=top_n)
    elif "AND" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("AND")]
        top_documents = find_top_documents_with_keyword_frequencies_and_json(json_file, keyword_list, top_n=top_n)
    else:
        keyword_list = [keywords.strip()]
        top_documents = find_top_documents_with_keyword_frequencies_or_json(json_file, keyword_list, top_n=top_n)

    return top_documents
