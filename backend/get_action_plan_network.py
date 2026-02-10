from neo4j import GraphDatabase
import json
from pathlib import Path
# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "dairynet"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_json(file_path):
    """Load JSON from a file and return list of documents, handling BOM if present."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(path, "r", encoding="utf-8-sig") as f:  # <- use utf-8-sig
        return json.load(f)
    
def build_action_plan_network_from_json(json_file, file_name, action):
    data = load_json(json_file)

    nodes = {}
    links = []

    # Filter for the given file and action
    filtered = [rec for rec in data if rec["fileName"] == file_name and rec["shortAction"] == action]

    for rec in filtered:
        file_name_val = rec["fileName"]
        short_action_val = rec["shortAction"]
        labels_list = rec.get("labels", [])

        # Node IDs
        file_node_id = f"file_{file_name_val.replace(' ', '_')}"
        short_action_node_id = f"shortaction_{short_action_val.replace(' ', '_')}"

        # Add File node
        if file_node_id not in nodes:
            nodes[file_node_id] = {
                "id": file_node_id,
                "label": file_name_val,
                "type": "File"
            }

        # Add Short Action node
        if short_action_node_id not in nodes:
            nodes[short_action_node_id] = {
                "id": short_action_node_id,
                "label": short_action_val,
                "type": "Short Action",
                "action": action
            }

        # Link File -> Short Action
        links.append({
            "source": file_node_id,
            "target": short_action_node_id,
            "type": "HAS_SHORTACTION"
        })

        # Add Label nodes and link Short Action -> Label
        for label in labels_list:
            label_node_id = f"label_{label.replace(' ', '_')}"
            if label_node_id not in nodes:
                nodes[label_node_id] = {
                    "id": label_node_id,
                    "label": label,
                    "type": "Label"
                }
            links.append({
                "source": short_action_node_id,
                "target": label_node_id,
                "type": "HAS_LABEL"
            })

    print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

    return {
        "graph": {
            "nodes": list(nodes.values()),
            "links": links
        }
    }

def get_carbon_action_plan_stakeholder_network(file_name: str, action: str):
    cypher_query = """
        MATCH (f:CARBON_AP_LONE_FILE {name: $file_name})-[:CARBON_AP_LONE_HAS_ACTION]->(a:CARBON_AP_LONE_ACTION {name: $action})
        OPTIONAL MATCH (a)-[:CARBON_AP_LONE_HAS_STAKEHOLDER]->(s:CARBON_AP_LONE_STAKEHOLDERS)
        OPTIONAL MATCH (s)-[:CARBON_AP_LONE_HAS_CATEGORY]->(c:CARBON_AP_LONE_CATEGORY)
        RETURN DISTINCT
            id(f) AS id_file, f.name AS label_file, 'File Name' AS type_file,
            id(a) AS id_action, a.name AS label_action, a.shortAction AS short_action_text, 'Action' AS type_action,
            id(s) AS id_stakeholder, s.name AS label_stakeholder, 'Formal Stakeholder' AS type_stakeholder,
            id(c) AS id_category, c.name AS label_category, 'Category' AS type_category
        ORDER BY label_file, label_action, label_stakeholder
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, file_name=file_name, action=action)

        nodes = {}
        links = []

        for record in results:
            for prefix in ['file', 'action', 'stakeholder', 'category']:
                node_id = record.get(f"id_{prefix}")
                if node_id is not None and node_id not in nodes:
                    if prefix == "action":
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record["short_action_text"],
                            "action": record["label_action"],
                            "type": "Short Action"
                        }
                    else:
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record.get(f"label_{prefix}"),
                            "type": record.get(f"type_{prefix}")
                        }

            # Add links if source and target exist
            if record.get("id_file") and record.get("id_action"):
                links.append({
                    "source": record["id_file"],
                    "target": record["id_action"],
                    "type": "CARBON_AP_LONE_HAS_ACTION"
                })

            if record.get("id_action") and record.get("id_stakeholder"):
                links.append({
                    "source": record["id_action"],
                    "target": record["id_stakeholder"],
                    "type": "CARBON_AP_LONE_HAS_STAKEHOLDER"
                })

            if record.get("id_stakeholder") and record.get("id_category"):
                links.append({
                    "source": record["id_stakeholder"],
                    "target": record["id_category"],
                    "type": "CARBON_AP_LONE_HAS_CATEGORY"
                })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching network data:", e)
        raise

def get_water_action_plan_stakeholder_network(file_name: str, action: str):
    cypher_query = """
        MATCH (f:WATER_AP_LONE_FILE {name: $file_name})-[:WATER_AP_LONE_HAS_ACTION]->(a:WATER_AP_LONE_ACTION {name: $action})
        OPTIONAL MATCH (a)-[:WATER_AP_LONE_HAS_STAKEHOLDER]->(s:WATER_AP_LONE_STAKEHOLDERS)
        OPTIONAL MATCH (s)-[:WATER_AP_LONE_HAS_CATEGORY]->(c:WATER_AP_LONE_CATEGORY)
        RETURN DISTINCT
            id(f) AS id_file, f.name AS label_file, 'File Name' AS type_file,
            id(a) AS id_action, a.name AS label_action, a.shortAction AS short_action_text, 'Action' AS type_action,
            id(s) AS id_stakeholder, s.name AS label_stakeholder, 'Formal Stakeholder' AS type_stakeholder,
            id(c) AS id_category, c.name AS label_category, 'Category' AS type_category
        ORDER BY label_file, label_action, label_stakeholder
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, file_name=file_name, action=action)

        nodes = {}
        links = []

        for record in results:
            for prefix in ['file', 'action', 'stakeholder', 'category']:
                node_id = record.get(f"id_{prefix}")
                if node_id is not None and node_id not in nodes:
                    if prefix == "action":
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record["short_action_text"],
                            "action": record["label_action"],
                            "type": "Short Action"
                        }
                    else:
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record.get(f"label_{prefix}"),
                            "type": record.get(f"type_{prefix}")
                        }

            # Add links if source and target exist
            if record.get("id_file") and record.get("id_action"):
                links.append({
                    "source": record["id_file"],
                    "target": record["id_action"],
                    "type": "WATER_AP_LONE_HAS_ACTION"
                })

            if record.get("id_action") and record.get("id_stakeholder"):
                links.append({
                    "source": record["id_action"],
                    "target": record["id_stakeholder"],
                    "type": "WATER_AP_LONE_HAS_STAKEHOLDER"
                })

            if record.get("id_stakeholder") and record.get("id_category"):
                links.append({
                    "source": record["id_stakeholder"],
                    "target": record["id_category"],
                    "type": "WATER_AP_LONE_HAS_CATEGORY"
                })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching network data:", e)
        raise

def get_live_action_plan_stakeholder_network(file_name: str, action: str):
    cypher_query = """
        MATCH (f:LIVE_AP_LONE_FILE {name: $file_name})-[:LIVE_AP_LONE_HAS_ACTION]->(a:LIVE_AP_LONE_ACTION {name: $action})
        OPTIONAL MATCH (a)-[:LIVE_AP_LONE_HAS_STAKEHOLDER]->(s:LIVE_AP_LONE_STAKEHOLDERS)
        OPTIONAL MATCH (s)-[:LIVE_AP_LONE_HAS_CATEGORY]->(c:LIVE_AP_LONE_CATEGORY)
        RETURN DISTINCT
            id(f) AS id_file, f.name AS label_file, 'File Name' AS type_file,
            id(a) AS id_action, a.name AS label_action, a.shortAction AS short_action_text, 'Action' AS type_action,
            id(s) AS id_stakeholder, s.name AS label_stakeholder, 'Formal Stakeholder' AS type_stakeholder,
            id(c) AS id_category, c.name AS label_category, 'Category' AS type_category
        ORDER BY label_file, label_action, label_stakeholder
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, file_name=file_name, action=action)

        nodes = {}
        links = []

        for record in results:
            for prefix in ['file', 'action', 'stakeholder', 'category']:
                node_id = record.get(f"id_{prefix}")
                if node_id is not None and node_id not in nodes:
                    if prefix == "action":
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record["short_action_text"],
                            "action": record["label_action"],
                            "type": "Short Action"
                        }
                    else:
                        nodes[node_id] = {
                            "id": node_id,
                            "label": record.get(f"label_{prefix}"),
                            "type": record.get(f"type_{prefix}")
                        }

            # Add links if source and target exist
            if record.get("id_file") and record.get("id_action"):
                links.append({
                    "source": record["id_file"],
                    "target": record["id_action"],
                    "type": "LIVE_AP_LONE_HAS_ACTION"
                })

            if record.get("id_action") and record.get("id_stakeholder"):
                links.append({
                    "source": record["id_action"],
                    "target": record["id_stakeholder"],
                    "type": "LIVE_AP_LONE_HAS_STAKEHOLDER"
                })

            if record.get("id_stakeholder") and record.get("id_category"):
                links.append({
                    "source": record["id_stakeholder"],
                    "target": record["id_category"],
                    "type": "LIVE_AP_LONE_HAS_CATEGORY"
                })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching network data:", e)
        raise

def get_carbon2_action_plan_stakeholder_network(file_name: str, action: str):
    return build_action_plan_network_from_json("static/data/carbon_ap.json", file_name, action)

def get_water2_action_plan_stakeholder_network(file_name: str, action: str):
    return build_action_plan_network_from_json("static/data/water_ap.json", file_name, action)

def get_live2_action_plan_stakeholder_network(file_name: str, action: str):
    return build_action_plan_network_from_json("static/data/live_ap.json", file_name, action)

def get_action_plan_network(query, file_name, action, access):
    if query == "car" and access == 'levelone':
        return get_carbon_action_plan_stakeholder_network(file_name, action)
    elif query == "wat" and access == 'levelone':
        return get_water_action_plan_stakeholder_network(file_name, action)
    elif query == "liv" and access == 'levelone':
        return get_live_action_plan_stakeholder_network(file_name, action)
    elif query == "car" and access == 'leveltwo':
        return get_carbon2_action_plan_stakeholder_network(file_name, action)
    elif query == "wat" and access == 'leveltwo':
        return get_water2_action_plan_stakeholder_network(file_name, action)
    elif query == "liv" and access == 'leveltwo':
        return get_live2_action_plan_stakeholder_network(file_name, action)
    else:
        return []