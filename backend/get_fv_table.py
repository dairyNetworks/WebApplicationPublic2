import json
from pathlib import Path

JSON_FOLDER = Path("static/data")

def load_json_file(file_name):
    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"JSON file not found: {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {path}: {e}")
        return []

def get_carbon2_fvr_json():
    data = load_json_file("carbon_fvnr.json")  # replace with your actual JSON filename
    table = []
    for record in data:
        table.append({
            "Mission": str(record.get("MISSION") or ""),
            "Mission Statement": str(record.get("MISSION STATEMENT") or ""),
            "Goal": str(record.get("GOAL") or ""),
            "Goal Statement": str(record.get("GOAL STATEMENT") or ""),
            "Action": str(record.get("ACTION") or ""),
            "Action Statement": str(record.get("ACTION STATEMENT") or ""),
            "Stakeholders": list(record.get("stakeholders") or [])
        })
    print(f"Loaded {len(data)} records from carbon_fvnr.json")

    return table

def get_water2_fvr_json():
    data = load_json_file("water_fvnr.json")  # replace with your actual JSON filename
    table = []
    for record in data:
        table.append({
            "Mission": str(record.get("MISSION") or ""),
            "Mission Statement": str(record.get("MISSION STATEMENT") or ""),
            "Goal": str(record.get("GOAL") or ""),
            "Goal Statement": str(record.get("GOAL STATEMENT") or ""),
            "Action": str(record.get("ACTION") or ""),
            "Action Statement": str(record.get("ACTION STATEMENT") or ""),
            "Stakeholders": list(record.get("stakeholders") or [])
        })
    return table

def get_livelihood2_fvr_json():
    data = load_json_file("live_fvnr.json")  # replace with your actual JSON filename
    table = []
    for record in data:
        table.append({
            "Mission": str(record.get("MISSION") or ""),
            "Mission Statement": str(record.get("MISSION STATEMENT") or ""),
            "Goal": str(record.get("GOAL") or ""),
            "Goal Statement": str(record.get("GOAL STATEMENT") or ""),
            "Action": str(record.get("ACTION") or ""),
            "Action Statement": str(record.get("ACTION STATEMENT") or ""),
            "Stakeholders": list(record.get("stakeholders") or [])
        })
    return table

def get_fv_table(query, access):
    """Return FVR data from JSON files, LTWO only."""
    if access != "leveltwo":
        return []  # we only handle LTWO here
    if query == "car":
        return get_carbon2_fvr_json()
    elif query == "wat":
        return get_water2_fvr_json()
    elif query == "liv":
        return get_livelihood2_fvr_json()
    else:
        return []
