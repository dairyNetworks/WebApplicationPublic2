import json
from pathlib import Path

JSON_FOLDER = Path("static/data")  # Folder containing your LTWO JSON files

def load_ltwo_json(query):
    """Load LTWO JSON file for the given query (car/wat/liv)"""
    file_map = {
        "car": "carbon_fvr_ltwo.json",
        #"wat": "water_fvr_ltwo.json",
        "liv": "live_fvr_ltwo.json"
    }
    file_name = file_map.get(query)
    if not file_name:
        print(f"❌ Unknown query: {query}")
        return []

    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"❌ File not found: {file_name}")
        return []

    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def get_ltwo_fvr_report_stakeholder(query, action):
    """Return report table for LTWO (level two) from JSON"""
    data = load_ltwo_json(query)
    table = []
    seen = set()

    for idx, record in enumerate(data, 1):
        try:
            # Filter by action
            record_action = record.get("a", {}).get("properties", {}).get("name")
            if record_action != action:
                continue

            row_tuple = (
                record.get("m", {}).get("properties", {}).get("name"),
                record.get("ms", {}).get("properties", {}).get("text"),
                record.get("g", {}).get("properties", {}).get("name"),
                record.get("gs", {}).get("properties", {}).get("text"),
                record.get("a", {}).get("properties", {}).get("name"),
                record.get("as", {}).get("properties", {}).get("text"),
                record.get("p", {}).get("properties", {}).get("name"),
                record.get("rs", {}).get("properties", {}).get("text"),
                record.get("l", {}).get("properties", {}).get("name")
            )

            if row_tuple not in seen:
                seen.add(row_tuple)
                table.append({
                    "Mission": row_tuple[0],
                    "Mission Statement": row_tuple[1],
                    "Goal": row_tuple[2],
                    "Goal Statement": row_tuple[3],
                    "Action": row_tuple[4],
                    "Action Statement": row_tuple[5],
                    "Initiative": row_tuple[6],
                    "Report Summary": row_tuple[7],
                    "Report Stakeholder": row_tuple[8]
                })
        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"✅ Total report rows: {len(table)}")
    return table

# Wrapper
def get_fvr_report(query, action, access):
    if access != "leveltwo":
        print("⚠️ Only LTWO JSON supported in this version")
        return []
    return get_ltwo_fvr_report_stakeholder(query, action)
