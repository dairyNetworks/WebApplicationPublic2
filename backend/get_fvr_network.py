from itertools import count
from pathlib import Path
import json

JSON_FOLDER = Path("static/data")  # Update this to your JSON folder

def load_json_file(file_name):
    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"❌ File not found: {file_name}")
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        try:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} records from {file_name}")
            return data
        except Exception as e:
            print(f"❌ Error loading JSON: {file_name}, Error: {e}")
            return []

def get_fvr_network(query: str, action: str, access: str):
    print(f"DEBUG: get_fv_network called with query={query}, action={action}, access={access}")

    file_map = {
        "car": "carbon_fvr.json",
        #"wat": "water_fvr.json",
        "liv": "live_fvr.json"
    }
    file_name = file_map.get(query)
    if not file_name:
        print(f"❌ Unknown query: {query}")
        return {"graph": {"nodes": [], "links": []}}

    data = load_json_file(file_name)
    if not data:
        print(f"❌ No data found for {query}")
        return {"graph": {"nodes": [], "links": []}}

    nodes = {}
    links = []
    node_ids = {}
    next_id = count(1)

    for idx, record in enumerate(data, 1):
        try:
            # Extract names from JSON nested structure
            record_mission = record.get("m", {}).get("properties", {}).get("name")
            record_goal = record.get("g", {}).get("properties", {}).get("name")
            record_action = record.get("a", {}).get("properties", {}).get("name")

            if record_action != action:
                continue

            # Add nodes
            for label, ntype in [
                (record_mission, "Mission"),
                (record_goal, "Goal"),
                (record_action, "Action")
            ]:
                if not label:
                    continue
                if label not in node_ids:
                    node_ids[label] = next(next_id)
                    nodes[node_ids[label]] = {"id": node_ids[label], "label": label, "type": ntype}

            # Add Mission -> Goal -> Action links
            if record_mission and record_goal:
                links.append({"source": node_ids[record_mission], "target": node_ids[record_goal], "type": "HAS_GOAL"})
            if record_goal and record_action:
                links.append({"source": node_ids[record_goal], "target": node_ids[record_action], "type": "HAS_ACTION"})

            # Add stakeholders from 's' and 'l' fields
            for stakeholder_field in ["s", "l"]:
                stakeholder_name = record.get(stakeholder_field, {}).get("properties", {}).get("name")
                if not stakeholder_name:
                    continue
                if stakeholder_name not in node_ids:
                    node_ids[stakeholder_name] = next(next_id)
                    nodes[node_ids[stakeholder_name]] = {"id": node_ids[stakeholder_name], "label": stakeholder_name, "type": "Stakeholder"}
                links.append({"source": node_ids[record_action], "target": node_ids[stakeholder_name], "type": "INVOLVES"})

        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {"graph": {"nodes": list(nodes.values()), "links": links}}
