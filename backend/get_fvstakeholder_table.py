import json
from pathlib import Path

# -------------------------------
# Load JSON files for each sector
# -------------------------------
DATA_FILES = {
    "car": Path("static/data/carbon_fvr.json"),
    "wat": Path("static/data/water_fvr.json"),
    "liv": Path("static/data/live_fvr.json")
}

SECTOR_DATA = {}

# Load JSON into memory
for sector, path in DATA_FILES.items():
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:  # utf-8-sig to handle BOM
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")

# -------------------------------
# Level-two FV stakeholder function
# -------------------------------
def get_ltwo_fvstakeholders(sector: str):
    """
    Returns all unique level-two stakeholders (labels) for a given sector.
    """
    data = SECTOR_DATA.get(sector, [])
    stakeholders = set()

    for record in data:
        # Each record may have a 's' or 'l' node for labels
        for key in ["s", "l"]:
            if key in record and "properties" in record[key]:
                name = record[key]["properties"].get("name")
                if name:
                    stakeholders.add(name)

    # Return sorted list of dicts like Neo4j version
    return [{"Formal Stakeholder": s} for s in sorted(stakeholders)]

# -------------------------------
# Unified interface
# -------------------------------
def get_fvstakeholder_table(query: str, access: str):
    """
    Returns level-two stakeholders for the given sector.
    
    query: 'car', 'wat', 'liv'
    access: must be 'leveltwo'
    """
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return []

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return []

    return get_ltwo_fvstakeholders(query)
