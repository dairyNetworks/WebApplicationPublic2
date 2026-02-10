import json
from pathlib import Path

JSON_FOLDER = Path("static/data")  # Folder containing your JSON files

def load_json(file_name):
    """Load LTWO JSON file for a given sector"""
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
            print(f"❌ Error loading JSON: {e}")
            return []

def extract_fw_network_from_json(data, recommendation: str, action: str):
    """Extract nodes and links for Recommendation → Action → Labels network"""
    nodes = {}
    links = []

    for idx, record in enumerate(data, 1):
        try:
            rec_node = record.get("n")
            act_node = record.get("m")
            label_node = record.get("l")  # Optional in JSON

            if not rec_node or not act_node:
                continue

            rec_props = rec_node.get("properties", {})
            act_props = act_node.get("properties", {})
            label_props = label_node.get("properties", {}) if label_node else {}

            # Match only the requested recommendation and action
            if rec_props.get("name") != recommendation or act_props.get("name") != action:
                continue

            # Add Recommendation node
            rec_id = rec_node.get("identity")
            if rec_id not in nodes:
                nodes[rec_id] = {
                    "id": rec_id,
                    "label": rec_props.get("shortRecommendation") or rec_props.get("name"),
                    "tooltip": rec_props.get("name"),
                    "type": "Recommendation"
                }

            # Add Action node
            act_id = act_node.get("identity")
            if act_id not in nodes:
                nodes[act_id] = {
                    "id": act_id,
                    "label": act_props.get("shortAction") or act_props.get("name"),
                    "tooltip": act_props.get("name"),
                    "type": "Action"
                }

            # Add Label/Stakeholder node
            if label_props:
                label_id = label_node.get("identity")
                if label_id not in nodes:
                    nodes[label_id] = {
                        "id": label_id,
                        "label": label_props.get("name"),
                        "tooltip": label_props.get("name"),
                        "type": "Label"
                    }

                # Add link Action → Label
                links.append({
                    "source": act_id,
                    "target": label_id,
                    "type": "ACTION_ASSIGNED_TO"
                })

            # Add link Recommendation → Action
            links.append({
                "source": rec_id,
                "target": act_id,
                "type": "RECOMMENDATION_HAS_ACTION"
            })

        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {"graph": {"nodes": list(nodes.values()), "links": links}}


# Sector-specific LTWO network functions
def get_carbon2_fw_network(recommendation: str, action: str):
    data = load_json("carbon_fw.json")
    return extract_fw_network_from_json(data, recommendation, action)

def get_water2_fw_network(recommendation: str, action: str):
    data = load_json("water_fw.json")
    return extract_fw_network_from_json(data, recommendation, action)

def get_live2_fw_network(recommendation: str, action: str):
    data = load_json("live_fw.json")
    return extract_fw_network_from_json(data, recommendation, action)


# Wrapper function
def get_fw_network(query, recommendation, action, access):
    if access != "leveltwo":
        print("⚠️ Only LTWO JSON supported in this version")
        return []

    if query == "car":
        return get_carbon2_fw_network(recommendation, action)
    elif query == "wat":
        return get_water2_fw_network(recommendation, action)
    elif query == "liv":
        return get_live2_fw_network(recommendation, action)
    else:
        return []
