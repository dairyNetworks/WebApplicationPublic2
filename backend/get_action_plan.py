import json
from pathlib import Path

# Load JSON safely (handles UTF-8 BOM)
def load_json(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

# Generic function to fetch LTWO action plan stakeholders from JSON
def get_ltwo_action_plan_stakeholder(json_file, file_name: str, action: str):
    data = load_json(json_file)
    table = []
    for record in data:
        if record.get("fileName") == file_name and record.get("shortAction") == action:
            for label in record.get("labels", []):
                table.append({
                    "File Name": file_name,
                    "Action": action,
                    "Stakeholder": label
                })
    return table

# Specific wrappers for each LTWO dataset
def get_carbon2_action_plan_stakeholder(file_name: str, action: str):
    return get_ltwo_action_plan_stakeholder("static/data/carbon_ap.json", file_name, action)

def get_water2_action_plan_stakeholder(file_name: str, action: str):
    return get_ltwo_action_plan_stakeholder("static/data/water_ap.json", file_name, action)

def get_livelihood2_action_plan_stakeholder(file_name: str, action: str):
    return get_ltwo_action_plan_stakeholder("static/data/live_ap.json", file_name, action)

# Dispatcher
def get_action_plan(query, file_name, action, access):
    if access != 'leveltwo':
        return []  # Only LTWO JSON-based supported here
    if query == "car":
        return get_carbon2_action_plan_stakeholder(file_name, action)
    elif query == "wat":
        return get_water2_action_plan_stakeholder(file_name, action)
    elif query == "liv":
        return get_livelihood2_action_plan_stakeholder(file_name, action)
    return []
