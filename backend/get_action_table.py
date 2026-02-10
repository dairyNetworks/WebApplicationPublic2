import json
from pathlib import Path

# ----------------------------
# Utility to load JSON data
# ----------------------------
def load_json(file_path):
    """Load JSON from a file and return list of documents, handling BOM if present."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, "r", encoding="utf-8-sig") as f:  # <- use utf-8-sig
        return json.load(f)

# ----------------------------
# Level 2 JSON-based action plan tables
# ----------------------------
def get_carbon2_action_plan():
    try:
        data = load_json("static/data/carbon_ap.json")
    except Exception as e:
        print("❌ Failed to load JSON:", e)
        return []

    print(f"✅ Loaded {len(data)} records")  # check how many records are read

    seen = set()
    table = []

    for rec in data:
        # Make sure keys exist
        file_name = rec.get("fileName")
        short_action = rec.get("shortAction")
        if not file_name or not short_action:
            print("⚠️ Skipping invalid record:", rec)
            continue

        key = (file_name, short_action)
        if key not in seen:
            seen.add(key)
            table.append({
                "Action Plan File": file_name,
                "Action": short_action
            })

    print(f"✅ Returning {len(table)} unique records")
    return table


def get_water2_action_plan():
    data = load_json("static/data/water_ap.json")
    seen = set()
    table = []

    for rec in data:
        key = (rec["fileName"], rec["shortAction"])
        if key not in seen:
            seen.add(key)
            table.append({
                "Action Plan File": rec["fileName"],
                "Action": rec["shortAction"]
            })
    return table

def get_livelihood2_action_plan():
    data = load_json("static/data/live_ap.json")
    seen = set()
    table = []

    for rec in data:
        key = (rec["fileName"], rec["shortAction"])
        if key not in seen:
            seen.add(key)
            table.append({
                "Action Plan File": rec["fileName"],
                "Action": rec["shortAction"]
            })
    return table

# ----------------------------
# Dispatcher
# ----------------------------
def get_action_table(query, access):
    if query == "car" and access == 'leveltwo':
        return get_carbon2_action_plan()
    elif query == "wat" and access == 'leveltwo':
        return get_water2_action_plan()
    elif query == "liv" and access == 'leveltwo':
        return get_livelihood2_action_plan()
    else:
        return []
