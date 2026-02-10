import json
from pathlib import Path

# Folder where JSON files are stored
JSON_FOLDER = Path("static/data")  # adjust as needed

def load_json_file(file_name):
    """Load JSON file and return a list of records."""
    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"File not found: {path}")
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def get_carbon2_fv_stakeholder_json(action: str):
    """Return Carbon LTWO stakeholder info for a given action."""
    data = load_json_file("carbon_fvnr.json")
    table = []
    for record in data:
        if record.get("ACTION") == action:
            for stakeholder in record.get("stakeholders", []):
                table.append({
                    "Mission": record.get("MISSION", ""),
                    "Mission Statement": record.get("MISSION STATEMENT", ""),
                    "Goal": record.get("GOAL", ""),
                    "Goal Statement": record.get("GOAL STATEMENT", ""),
                    "Action": record.get("ACTION", ""),
                    "Action Statement": record.get("ACTION STATEMENT", ""),
                    "Stakeholder": stakeholder
                })
    return table

def get_water2_fv_stakeholder_json(action: str):
    """Return Water LTWO stakeholder info for a given action."""
    data = load_json_file("water_fvnr.json")
    table = []
    for record in data:
        if record.get("ACTION") == action:
            for stakeholder in record.get("stakeholders", []):
                table.append({
                    "Mission": record.get("MISSION", ""),
                    "Mission Statement": record.get("MISSION STATEMENT", ""),
                    "Goal": record.get("GOAL", ""),
                    "Goal Statement": record.get("GOAL STATEMENT", ""),
                    "Action": record.get("ACTION", ""),
                    "Action Statement": record.get("ACTION STATEMENT", ""),
                    "Stakeholder": stakeholder
                })
    return table

def get_livelihood2_fv_stakeholder_json(action: str):
    """Return Livelihood LTWO stakeholder info for a given action."""
    data = load_json_file("live_fvnr.json")
    table = []
    for record in data:
        if record.get("ACTION") == action:
            for stakeholder in record.get("stakeholders", []):
                table.append({
                    "Mission": record.get("MISSION", ""),
                    "Mission Statement": record.get("MISSION STATEMENT", ""),
                    "Goal": record.get("GOAL", ""),
                    "Goal Statement": record.get("GOAL STATEMENT", ""),
                    "Action": record.get("ACTION", ""),
                    "Action Statement": record.get("ACTION STATEMENT", ""),
                    "Stakeholder": stakeholder
                })
    return table

def get_fv(query: str, action: str, access: str):
    """Main entry point for LTWO JSON stakeholder data."""
    if query == "car":
        return get_carbon2_fv_stakeholder_json(action)
    elif query == "wat":
        return get_water2_fv_stakeholder_json(action)
    elif query == "liv":
        return get_livelihood2_fv_stakeholder_json(action)
    else:
        return []
