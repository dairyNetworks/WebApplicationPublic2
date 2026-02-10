from pathlib import Path
import json

JSON_FOLDER = Path("static/data")  # folder containing your JSON files

def load_fw_json(file_name):
    """Load LTWO JSON file for a given sector"""
    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"❌ File not found: {file_name}")
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        try:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} records from {file_name}")
            return data
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return []

def extract_fw_from_json(data, recommendation: str, action: str):
    """Extract Recommendation → Action → Stakeholder/Label table from JSON"""
    table = []
    for idx, record in enumerate(data, 1):
        try:
            rec_node = record.get("n")
            act_node = record.get("m")
            label_node = record.get("l")  # In your JSON, label/stakeholder is optional

            if not rec_node or not act_node:
                continue

            rec_props = rec_node.get("properties", {})
            act_props = act_node.get("properties", {})
            label_props = label_node.get("properties", {}) if label_node else {}

            # Match only the requested recommendation and action
            if rec_props.get("name") != recommendation or act_props.get("name") != action:
                continue

            table.append({
                "Recommendation": rec_props.get("name"),
                "Action": act_props.get("name"),
                "Stakeholder": label_props.get("name")
            })
        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")
    print(f"✅ Total rows extracted: {len(table)}")
    return table

# LTWO only functions
def get_carbon2_fw(recommendation: str, action: str):
    data = load_fw_json("carbon_fw.json")
    return extract_fw_from_json(data, recommendation, action)

def get_water2_fw(recommendation: str, action: str):
    data = load_fw_json("water_fw.json")
    return extract_fw_from_json(data, recommendation, action)

def get_live2_fw(recommendation: str, action: str):
    data = load_fw_json("live_fw.json")
    return extract_fw_from_json(data, recommendation, action)

# Wrapper function
def get_fw(query: str, recommendation: str, action: str, access: str):
    if access != "leveltwo":
        print("⚠️ Only LTWO JSON supported in this version")
        return []

    if query == "car":
        return get_carbon2_fw(recommendation, action)
    elif query == "wat":
        return get_water2_fw(recommendation, action)
    elif query == "liv":
        return get_live2_fw(recommendation, action)
    else:
        return []
