import json
from pathlib import Path

# -------------------------------
# Load level-two JSON files
# -------------------------------
DATA_FILES = {
    "car": Path("static/data/carbon_fvr.json"),
    "wat": Path("static/data/water_fvr.json"),
    "liv": Path("static/data/live_fvr.json")
}

SECTOR_DATA = {}

for sector, path in DATA_FILES.items():
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")


# -------------------------------
# Level-two network function
# -------------------------------
def get_ltwo_fvstakeholder_network(sector: str, formalStakeholder: str):
    """
    Returns a node-link network graph for a level-two stakeholder from JSON.
    """
    data = SECTOR_DATA.get(sector, [])
    nodes = {}
    links = []

    for record in data:
        # Check if formalStakeholder matches 's' or 'l' labels
        stakeholder_names = []
        for key in ["s", "l"]:
            if key in record and "properties" in record[key]:
                name = record[key]["properties"].get("name")
                if name:
                    stakeholder_names.append(name)

        if formalStakeholder not in stakeholder_names:
            continue

        # Add nodes
        for key, node_type in [("l", "Formal Stakeholder"), ("m", "Mission"), ("g", "Goal"), ("a", "Action")]:
            if key in record and "properties" in record[key]:
                node_id = record[key]["identity"]
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": record[key]["properties"].get("name"),
                        "type": node_type
                    }

        # Add links (following ltwo network structure)
        links.append({
            "source": record["a"]["identity"],
            "target": record["l"]["identity"],
            "type": f"{sector.upper()}_FVRA_LTWO_ACTION_LABEL_LINK"
        })
        links.append({
            "source": record["g"]["identity"],
            "target": record["a"]["identity"],
            "type": f"{sector.upper()}_FVRA_LTWO_GOALACTION_LINK"
        })
        links.append({
            "source": record["m"]["identity"],
            "target": record["g"]["identity"],
            "type": f"{sector.upper()}_FVRA_LTWO_MISSIONGOAL_LINK"
        })

    print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {
        "graph": {
            "nodes": list(nodes.values()),
            "links": links
        }
    }


# -------------------------------
# Unified interface
# -------------------------------
def get_fvstakeholder_network(query: str, formalStakeholder: str, access: str):
    """
    Returns level-two FV stakeholder network.
    Only 'leveltwo' supported in this version.
    """
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return []

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return []

    return get_ltwo_fvstakeholder_network(query, formalStakeholder)
