import json
from pathlib import Path

# -------------------------------
# Load JSON files for each sector
# -------------------------------
DATA_FILES = {
    "car": Path("static/data/carbon_ap.json"),
    "wat": Path("static/data/water_ap.json"),
    "liv": Path("static/data/live_ap.json")
}

SECTOR_DATA = {}

# Load JSON into memory
for sector, path in DATA_FILES.items():
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")

# -------------------------------
# Level-two action-stakeholder function
# -------------------------------
def get_l2_actionstakeholder_plan_stakeholder(sector: str, formalStakeholder: str):
    """
    Returns all actions for a given stakeholder from the level-two JSON data.
    """
    table = []
    data = SECTOR_DATA.get(sector, [])

    for record in data:
        if formalStakeholder in record.get("labels", []):
            table.append({
                "Label": formalStakeholder,
                "File": record.get("fileName"),
                "Action": record.get("shortAction")
            })
    return table

# -------------------------------
# Unified interface function
# -------------------------------
def get_actionstakeholder_plan(query: str, formalStakeholder: str, access: str):
    """
    Returns level-two actions for a stakeholder.
    Only leveltwo ('ltwo') supported in this version.
    
    query: 'car', 'wat', 'liv'
    access: must be 'leveltwo'
    """
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return []

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return []

    return get_l2_actionstakeholder_plan_stakeholder(query, formalStakeholder)
