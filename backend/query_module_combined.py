import json
import unicodedata
import re
from pathlib import Path

# --------------------------
# Utility functions
# --------------------------
def clean(t):
    """Normalize strings for comparison."""
    if isinstance(t, str):
        t = unicodedata.normalize("NFKD", t)
        return re.sub(r'[.\-\s]', '', t.lower().strip())
    return t

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
def find_top_documents_with_keyword_frequencies_or(all_docs, keywords, top_n=5):
    """Find top documents where any of the keywords exist."""
    keywords = [kw.replace(" ", "_") for kw in keywords]

    # Filter documents: OR condition
    filtered_docs = [
        doc for doc in all_docs
        if any(doc.get("term_document_matrix_dept", {}).get(kw, 0) > 0 for kw in keywords)
    ]

    # Compute total frequency
    for doc in filtered_docs:
        doc["TotalFrequency"] = sum(doc.get("term_document_matrix_dept", {}).get(kw, 0) for kw in keywords)
        doc["count"] = 1
        for kw in keywords:
            doc[kw] = doc.get("term_document_matrix_dept", {}).get(kw, 0)

    # Sort by frequency and limit
    top_docs = sorted(filtered_docs, key=lambda x: x["TotalFrequency"], reverse=True)[:top_n]
    return top_docs

def find_top_documents_with_keyword_frequencies_and(all_docs, keywords, top_n=5):
    """Find top documents where all keywords exist."""
    keywords = [kw.replace(" ", "_") for kw in keywords]

    # Filter documents: AND condition
    filtered_docs = [
        doc for doc in all_docs
        if all(doc.get("term_document_matrix_dept", {}).get(kw, 0) > 0 for kw in keywords)
    ]

    # Compute total frequency
    for doc in filtered_docs:
        doc["TotalFrequency"] = sum(doc.get("term_document_matrix_dept", {}).get(kw, 0) for kw in keywords)
        doc["count"] = 1
        for kw in keywords:
            doc[kw] = doc.get("term_document_matrix_dept", {}).get(kw, 0)

    # Sort by frequency and limit
    top_docs = sorted(filtered_docs, key=lambda x: x["TotalFrequency"], reverse=True)[:top_n]
    return top_docs

# --------------------------
# Combined function logic
# --------------------------
def function_call_combined_l1(keywords, json_file="static/data/P1_speaker_speech.json", speaker_json_file="static/data/speaker_info_2.json", top_n=5):
    # Load JSON data
    all_docs = load_json(json_file)
    speaker_info = load_json(speaker_json_file)
    speaker_dict = {doc.get("Labels"): doc for doc in speaker_info}

    # Determine keyword logic
    if "OR" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("OR")]
        top_documents = find_top_documents_with_keyword_frequencies_or(all_docs, keyword_list, top_n=top_n)
    elif "AND" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("AND")]
        top_documents = find_top_documents_with_keyword_frequencies_and(all_docs, keyword_list, top_n=top_n)
    else:
        keyword_list = [keywords.strip()]
        top_documents = find_top_documents_with_keyword_frequencies_or(all_docs, keyword_list, top_n=top_n)

    # Enrich with speaker info
    for doc in top_documents:
        labels = doc.get("Labels")
        additional_info = speaker_dict.get(labels)
        if additional_info:
            doc["Organization"] = additional_info.get("Organization")
            doc["Designation"] = additional_info.get("Designation")

    return top_documents

def function_call_combined_l2(keywords, json_file="static/data/P1_speaker_speech.json", speaker_json_file="static/data/speaker_info_2.json", top_n=5):
    # Load JSON data
    all_docs = load_json(json_file)
    speaker_info = load_json(speaker_json_file)
    speaker_dict = {clean(doc.get("Speaker")): doc for doc in speaker_info}

    # Determine keyword logic
    if "OR" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("OR")]
        top_documents = find_top_documents_with_keyword_frequencies_or(all_docs, keyword_list, top_n=top_n)
    elif "AND" in keywords:
        keyword_list = [kw.strip() for kw in keywords.split("AND")]
        top_documents = find_top_documents_with_keyword_frequencies_and(all_docs, keyword_list, top_n=top_n)
    else:
        keyword_list = [keywords.strip()]
        top_documents = find_top_documents_with_keyword_frequencies_or(all_docs, keyword_list, top_n=top_n)

    # Enrich with speaker info using normalized names
    for doc in top_documents:
        speaker_name = doc.get("Speaker")
        norm_speaker = clean(speaker_name)
        additional_info = speaker_dict.get(norm_speaker)
        if additional_info:
            doc["Organization"] = additional_info.get("Organization")
            doc["Designation"] = additional_info.get("Designation")

    return top_documents

def function_call_combined(keywords, access="levelone", top_n=5):
    if access == "levelone":
        return function_call_combined_l1(keywords, top_n=top_n)
    elif access == "leveltwo":
        return function_call_combined_l2(keywords, top_n=top_n)
