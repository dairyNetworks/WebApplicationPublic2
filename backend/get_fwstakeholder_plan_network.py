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
    if path.exists():
        with open(path, "r", encoding="utf-8-sig") as f:
            SECTOR_DATA[sector] = json.load(f)
    else:
        SECTOR_DATA[sector] = []
        print(f"⚠️ JSON file not found for {sector}: {path}")


# -------------------------------
# Level-two FW stakeholder network
# -------------------------------
def get_ltwo_fwstakeholder_network(sector: str, formalStakeholder: str):
    data = SECTOR_DATA.get(sector, [])
    print(f"⚠️ Processing sector '{sector}' for stakeholder '{formalStakeholder}' with {len(data)} records")

    nodes = {}
    links = []

    for idx, record in enumerate(data):
        try:
            m_node = record.get("m") or {}
            m_name = (m_node.get("properties") or {}).get("name")
            if not m_name or m_name != formalStakeholder:
                continue
            s_id = f"m_{m_node.get('identity', idx)}"
            nodes[s_id] = {
                "id": s_id,
                "label": m_name,
                "fullLabel": m_name,
                "type": "Stakeholder"
            }

            n_node = record.get("n") or {}
            n_props = n_node.get("properties") or {}
            action_name = n_props.get("name", f"Action {idx}")
            a_id = f"n_{n_node.get('identity', idx)}"
            nodes[a_id] = {
                "id": a_id,
                "label": action_name,
                "fullLabel": action_name,
                "type": "Action"
            }

            r_node = record.get("r") or {}
            r_props = r_node.get("properties") or {}
            rec_name = r_props.get("name")
            r_id = f"r_{r_node.get('identity', idx)}" if r_node else None
            if r_node and r_id not in nodes:
                nodes[r_id] = {
                    "id": r_id,
                    "label": rec_name or f"Recommendation {idx}",
                    "fullLabel": rec_name or f"Recommendation {idx}",
                    "type": "Recommendation"
                }

            # -------------------------------
            # Create links
            # -------------------------------
            if r_id:
                links.append({
                    "source": s_id,
                    "target": r_id,
                    "type": f"{sector.upper()}_LTWO_FWSTAKEHOLDER_HAS_RECOMMENDATION"
                })
                links.append({
                    "source": r_id,
                    "target": a_id,
                    "type": f"{sector.upper()}_LTWO_FWSTAKEHOLDER_HAS_ACTION"
                })
            else:
                # No recommendation node, link Stakeholder -> Action directly
                links.append({
                    "source": s_id,
                    "target": a_id,
                    "type": f"{sector.upper()}_LTWO_FWSTAKEHOLDER_HAS_ACTION"
                })

        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")
            continue

    print(f"✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {"graph": {"nodes": list(nodes.values()), "links": links}}
 


# -------------------------------
# Unified interface
# -------------------------------
def get_fwstakeholder_plan_network(query, formalStakeholder, access):
    if access != "leveltwo":
        print("⚠️ Only leveltwo supported in this version")
        return {}

    if query not in SECTOR_DATA:
        print(f"⚠️ Unknown sector '{query}'")
        return {}

    return get_ltwo_fwstakeholder_network(query, formalStakeholder)
