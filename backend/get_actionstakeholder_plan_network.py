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

for sector, path in DATA_FILES.items():
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")

def get_l2_actionstakeholder_plan_stakeholder_network(
    sector: str,
    formalStakeholder: str
):
    """
    Builds a graph network (nodes + links) for a given stakeholder
    from level-two JSON data.
    """

    data = SECTOR_DATA.get(sector, [])
    nodes = {}
    links = []

    for record in data:
        labels = record.get("labels", [])
        if formalStakeholder not in labels:
            continue

        file_name = record.get("fileName")
        short_action = record.get("shortAction")
        full_action = record.get("action", "")

        # Stable node IDs
        file_id = f"file_{file_name.replace(' ', '_')}"
        action_id = f"shortaction_{short_action.replace(' ', '_')}"

        # -----------------
        # File node
        # -----------------
        if file_id not in nodes:
            nodes[file_id] = {
                "id": file_id,
                "label": file_name,
                "type": "File"
            }

        # -----------------
        # Short Action node
        # -----------------
        if action_id not in nodes:
            nodes[action_id] = {
                "id": action_id,
                "label": short_action,
                "type": "Short Action",
                "action": full_action
            }

        # File → Action
        links.append({
            "source": file_id,
            "target": action_id,
            "type": "HAS_SHORTACTION"
        })

        # -----------------
        # Label nodes
        # -----------------
        for label in labels:
            label_id = f"label_{label.replace(' ', '_')}"

            if label_id not in nodes:
                nodes[label_id] = {
                    "id": label_id,
                    "label": label,
                    "type": "Label"
                }

            links.append({
                "source": action_id,
                "target": label_id,
                "type": "HAS_LABEL"
            })

    print(f"✅ L2 {sector.upper()} | Nodes: {len(nodes)} | Links: {len(links)}")

    return {
        "graph": {
            "nodes": list(nodes.values()),
            "links": links
        }
    }

def get_actionstakeholder_plan_network(
    query: str,
    formalStakeholder: str,
    access: str
):
    """
    Unified interface for L2 stakeholder network.

    query: 'car', 'wat', 'liv'
    access: must be 'leveltwo'
    """

    if access != "leveltwo":
        print("⚠️ Only leveltwo supported for network view")
        return {"graph": {"nodes": [], "links": []}}

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return {"graph": {"nodes": [], "links": []}}

    return get_l2_actionstakeholder_plan_stakeholder_network(
        query,
        formalStakeholder
    )
