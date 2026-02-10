import json
from pathlib import Path

# -------------------------------
# Load JSON files for each sector (level-two)
# -------------------------------
DATA_FILES = {
    "car": Path("static/data/carbon_fvr.json"),
    "wat": Path("static/data/water_fvr.json"),
    "liv": Path("static/data/live_fvr.json")
}

SECTOR_DATA = {}

for sector, path in DATA_FILES.items():
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:  # handle BOM
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")


# -------------------------------
# Level-two FV stakeholder function
# -------------------------------
def get_ltwo_fvstakeholder(sector: str, formalStakeholder: str):
    """
    Returns all missions, goals, actions, and statements for a given level-two stakeholder.
    """
    data = SECTOR_DATA.get(sector, [])
    table = []

    for record in data:
        # Some records have multiple labels ('s' and 'l')
        labels = []
        for key in ["s", "l"]:
            if key in record and "properties" in record[key]:
                name = record[key]["properties"].get("name")
                if name:
                    labels.append(name)

        # Check if formalStakeholder matches any label
        if formalStakeholder in labels:
            table.append({
                "Stakeholder": formalStakeholder,
                "Mission": record.get("m", {}).get("properties", {}).get("name"),
                "Mission Statement": record.get("ms", {}).get("properties", {}).get("text"),
                "Goal": record.get("g", {}).get("properties", {}).get("name"),
                "Goal Statement": record.get("gs", {}).get("properties", {}).get("text"),
                "Action": record.get("a", {}).get("properties", {}).get("name"),
                "Action Statement": record.get("as", {}).get("properties", {}).get("text")
            })

    # Sort by Mission -> Goal -> Action
    table.sort(key=lambda x: (x["Mission"] or "", x["Goal"] or "", x["Action"] or ""))
    return table


# -------------------------------
# Unified interface
# -------------------------------
def get_fvstakeholder_plan(query: str, formalStakeholder: str, access: str):
    """
    Returns level-two FV stakeholder details for the given sector.
    Only 'leveltwo' supported.
    """
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return []

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return []

    return get_ltwo_fvstakeholder(query, formalStakeholder)
