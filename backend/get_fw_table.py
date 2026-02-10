from pathlib import Path
import json

JSON_FOLDER = Path("static/data")  # folder containing your JSON files

def load_fw_json(file_name):
    """Load JSON file for any network"""
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

def extract_fw_table(data):
    """Extract Recommendation → Action table from JSON"""
    table = []
    for idx, record in enumerate(data, 1):
        try:
            recommendation_node = record.get("n")  # Recommendation
            action_node = record.get("m")         # Action

            if not recommendation_node or not action_node:
                continue

            rec_props = recommendation_node.get("properties", {})
            act_props = action_node.get("properties", {})

            table.append({
                "Recommendation": rec_props.get("name"),
                "ShortRecommendation": rec_props.get("shortRecommendation"),
                "Action": act_props.get("name"),
                "ShortAction": act_props.get("shortAction")
            })
        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")
    print(f"✅ Total rows extracted: {len(table)}")
    return table

# Now replace your Neo4j functions
def get_carbon2_fw():
    data = load_fw_json("carbon_fw.json")
    return extract_fw_table(data)

def get_water2_fw():
    data = load_fw_json("water_fw.json")
    return extract_fw_table(data)

def get_livelihood2_fw():
    data = load_fw_json("live_fw.json")
    return extract_fw_table(data)

def get_fw_table(query, access):
    if access != "leveltwo":
        print("⚠️ Only LTWO JSON supported in this version")
        return []

    if query == "car":
        return get_carbon2_fw()
    elif query == "wat":
        return get_water2_fw()
    elif query == "liv":
        return get_livelihood2_fw()
    else:
        return []
