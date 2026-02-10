import json
from pathlib import Path

# Folder where JSON files are stored
JSON_FOLDER = Path("static/data")  # adjust path as needed

def load_json(file_name):
    """Load JSON file"""
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

def extract_leveltwo_stakeholders_from_json(data):
    """Extract distinct stakeholders from leveltwo JSON"""
    stakeholders_set = set()
    for record in data:
        labels = record.get("labels", [])
        for label in labels:
            stakeholders_set.add(label.strip())  # remove extra spaces
    # Return sorted list of dictionaries (like Neo4j version)
    return [{"Formal Stakeholder": s} for s in sorted(stakeholders_set)]

# Sector-specific leveltwo functions
def get_carbon_leveltwo_actionstakeholder_plan():
    data = load_json("carbon_ap.json")  # replace with your actual file name
    return extract_leveltwo_stakeholders_from_json(data)

def get_water_leveltwo_actionstakeholder_plan():
    data = load_json("water_ap.json")
    return extract_leveltwo_stakeholders_from_json(data)

def get_livelihood_leveltwo_actionstakeholder_plan():
    data = load_json("live_ap.json")
    return extract_leveltwo_stakeholders_from_json(data)

# Wrapper function
def get_actionstakeholder_table(query, access):
    if access != 'leveltwo':
        print("⚠️ Only leveltwo JSON supported in this version")
        return []

    if query == "car":
        return get_carbon_leveltwo_actionstakeholder_plan()
    elif query == "wat":
        return get_water_leveltwo_actionstakeholder_plan()
    elif query == "liv":
        return get_livelihood_leveltwo_actionstakeholder_plan()
    else:
        return []
