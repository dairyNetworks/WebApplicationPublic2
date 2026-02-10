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

def get_fv_network(query: str, action: str, access: str):
    print(f"DEBUG: get_fv_network called with query={query}, action={action}, access={access}")
    
    if access not in ["levelone", "leveltwo"]:
        print(f"⚠️ Unknown access level: {access}, defaulting to levelone")
        access = "levelone"
    
    file_map = {
        "car": "carbon_fvnr.json",
        "wat": "water_fvnr.json",
        "liv": "live_fvnr.json"
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
        print(f"\n--- Processing record {idx} ---")
        print(f"Record keys: {list(record.keys())}")  # debug
        try:
            # Use uppercase keys from JSON
            record_action = record.get("ACTION")
            record_mission = record.get("MISSION")
            record_goal = record.get("GOAL")
            print(f"ACTION in record: {record_action}")

            if record_action != action:
                print(f"Skipping record because action does not match")
                continue

            # Add nodes for Mission, Goal, Action
            for label, ntype in [
                (record_mission, "Mission"),
                (record_goal, "Goal"),
                (record_action, "Action")
            ]:
                if not label:
                    print(f"⚠️ Missing {ntype} field, skipping node")
                    continue
                if label not in node_ids:
                    node_ids[label] = next(next_id)
                    nodes[node_ids[label]] = {"id": node_ids[label], "label": label, "type": ntype}
                    print(f"Added node {label} with id {node_ids[label]}")

            # Add links Mission -> Goal -> Action
            if record_mission and record_goal:
                links.append({"source": node_ids[record_mission], "target": node_ids[record_goal], "type": "HAS_GOAL"})
                print(f"Added link: {record_mission} -> {record_goal}")
            if record_goal and record_action:
                links.append({"source": node_ids[record_goal], "target": node_ids[record_action], "type": "HAS_ACTION"})
                print(f"Added link: {record_goal} -> {record_action}")

            # Stakeholders
            stakeholders = record.get("stakeholders", [])
            if not isinstance(stakeholders, list):
                stakeholders = [stakeholders]

            for stakeholder in stakeholders:
                if not stakeholder:
                    continue
                if stakeholder not in node_ids:
                    node_ids[stakeholder] = next(next_id)
                    nodes[node_ids[stakeholder]] = {"id": node_ids[stakeholder], "label": stakeholder, "type": "Stakeholder"}
                    print(f"Added stakeholder node {stakeholder} with id {node_ids[stakeholder]}")
                links.append({"source": node_ids[record_action], "target": node_ids[stakeholder], "type": "INVOLVES"})
                print(f"Added link: {record_action} -> {stakeholder}")

        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {"graph": {"nodes": list(nodes.values()), "links": links}}
