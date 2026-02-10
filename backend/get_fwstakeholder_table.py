import json
from pathlib import Path

# -------------------------------
# Load level-two JSON files
# -------------------------------
DATA_FILES = {
    "car": Path("static/data/carbon_fw.json"),
    "wat": Path("static/data/water_fw.json"),
    "liv": Path("static/data/live_fw.json")
}

SECTOR_DATA = {}

for sector, path in DATA_FILES.items():
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8-sig") as f:
                SECTOR_DATA[sector] = json.load(f)
            print(f"✅ Loaded {len(SECTOR_DATA[sector])} records for '{sector}' from {path}")
        else:
            SECTOR_DATA[sector] = []
            print(f"⚠️ JSON file not found for {sector}: {path}")
    except json.JSONDecodeError as e:
        SECTOR_DATA[sector] = []
        print(f"❌ JSON decode error for {sector}: {e}")
    except Exception as e:
        SECTOR_DATA[sector] = []
        print(f"❌ Unexpected error loading {sector}: {e}")

# -------------------------------
# Level-two FW stakeholder table
# -------------------------------
def get_ltwo_fwstakeholder_table(sector: str):
    try:
        data = SECTOR_DATA.get(sector, [])
        print(f"⚠️ Processing sector '{sector}' with {len(data)} records")

        table = []
        seen = set()

        for idx, record in enumerate(data):
            if not isinstance(record, dict):
                print(f"⚠️ Skipping invalid record at index {idx}: not a dict")
                continue

            if "m" in record and isinstance(record["m"], dict):
                props = record["m"].get("properties")
                if props and isinstance(props, dict):
                    name = props.get("name")
                    if name and name not in seen:
                        table.append({"Formal Stakeholder": name})
                        seen.add(name)
                else:
                    print(f"⚠️ Missing or invalid 'properties' in record at index {idx}")
            else:
                print(f"⚠️ Missing 'm' node in record at index {idx}")

        table.sort(key=lambda x: x["Formal Stakeholder"])
        return table

    except Exception as e:
        print(f"❌ Error processing sector '{sector}': {e}")
        raise  # Keep raising so FastAPI returns 500 for visibility

# -------------------------------
# Unified interface
# -------------------------------
def get_fwstakeholder_table(query: str, access: str):
    try:
        if access != "leveltwo":
            print("⚠️ Only leveltwo supported in this version")
            return []

        if query not in SECTOR_DATA:
            print(f"⚠️ Unknown sector '{query}'")
            return []

        return get_ltwo_fwstakeholder_table(query)

    except Exception as e:
        print(f"❌ Error in get_fwstakeholder_table(query={query}, access={access}): {e}")
        raise
