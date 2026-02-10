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
            print(f"✅ Loaded {len(SECTOR_DATA[sector])} records for '{sector}'")
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
# Level-two FW stakeholder plan table
# -------------------------------
def get_ltwo_fwstakeholder_plan(sector: str, formalStakeholder: str):
    """
    Returns table of Actions + Recommendations for a level-two stakeholder from JSON.
    """
    try:
        data = SECTOR_DATA.get(sector, [])
        print(f"⚠️ Processing sector '{sector}' for stakeholder '{formalStakeholder}' with {len(data)} records")

        table = []

        for idx, record in enumerate(data):
            # Check 'm' node for stakeholder/label match
            m_node = record.get("m") or {}
            m_props = m_node.get("properties") or {}
            m_name = m_props.get("name")
            if not m_name:
                continue  # Skip invalid records

            if m_name != formalStakeholder:
                continue  # Skip non-matching stakeholder

            # Safely extract Action and Recommendation from 'n' and 'r'
            n_node = record.get("n") or {}
            r_node = record.get("r") or {}

            action_name = (n_node.get("properties") or {}).get("name", "")
            recommendation_name = (r_node.get("properties") or {}).get("name", "")

            table.append({
                "Stakeholder": m_name,
                "Action": action_name,
                "Recommendation": recommendation_name
            })

        # Optional: sort by Recommendation then Action
        table.sort(key=lambda x: (x["Recommendation"], x["Action"]))
        return table

    except Exception as e:
        print(f"❌ Error processing {sector} / {formalStakeholder}: {e}")
        return []



# -------------------------------
# Unified interface
# -------------------------------
def get_fwstakeholder_plan(query: str, formalStakeholder: str, access: str):
    """
    Only level-two supported in this version
    """
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return []

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return []

    return get_ltwo_fwstakeholder_plan(query, formalStakeholder)
