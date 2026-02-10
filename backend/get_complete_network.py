import csv
import json
from pathlib import Path

# ---- CONFIG ----
MAPPING_CSV = "static/data/stakeholders.csv"
JSON_DIR = "static/data"

def get_complete_network(label: str, query: str):
    # Map query to topic
    topic_map = {
        "car": "carbon",
        "wat": "water",
        "liv": "live"
    }
    topic_filter = topic_map.get(query.lower(), query.lower())

    # ---- Step 1: Resolve JSON file from CSV mapping ----
    mapping_file = Path(MAPPING_CSV)
    json_filename = None

    try:
        with open(mapping_file, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Labels"].strip() == label:
                    json_filename = row["Maping"].strip()
                    break
        if not json_filename:
            raise FileNotFoundError(f"No mapping found for label '{label}' in CSV")
        if not json_filename.lower().endswith(".json"):
            json_filename += ".json"
    except Exception as e:
        print(f"❌ Error reading mapping CSV: {e}")
        raise

    # ---- Step 2: Load JSON file ----
    json_path = Path(JSON_DIR) / json_filename
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    try:
        with open(json_path, encoding="utf-8-sig") as f:
            records = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON file {json_path}: {e}")
        raise

    # ---- Step 3: Build network ----
    nodes = {}
    links = []
    seen_links = set()

    def add_node_and_link(node_id, label, node_type, source_id=None, link_type=None, tooltip=None):
        if node_id is None:
            return
        if node_id not in nodes:
            node = {
                "id": node_id,
                "label": label or "Unknown",
                "type": node_type
            }
            if tooltip:
                node["tooltip"] = tooltip
            nodes[node_id] = node

        if source_id is not None and link_type is not None:
            link_key = (source_id, node_id, link_type)
            if link_key not in seen_links:
                links.append({"source": source_id, "target": node_id, "type": link_type})
                seen_links.add(link_key)

    # ---- Step 4: Process records ----
    for record in records:
        # Filter by topic if applicable
        def match_topic(r):
            return r and r.get("properties", {}).get("topic") == topic_filter

        l = record.get("l")
        if l:
            l_id = l.get("identity")
            l_name = l.get("properties", {}).get("name", label)
            add_node_and_link(l_id, l_name, "Label")

            # Action Plan
            a1 = record.get("r1") if match_topic(record.get("r1")) else record.get("a1") or record.get("r1")
            a2 = record.get("r1") if match_topic(record.get("r2")) else record.get("a2")
            a4 = record.get("a4")
            p5 = record.get("p5")

        # Iterate all nodes in the JSON (l, r1, n1, r2, n2)
        for key in ["l", "n1", "n2"]:
            node = record.get(key)
            if node:
                node_id = node.get("identity")
                node_props = node.get("properties", {})
                node_label = node_props.get("name") or node_props.get("label") or key
                node_type = node.get("labels", ["Node"])[0]
                add_node_and_link(node_id, node_label, node_type)

        # Iterate all relationships
        for key in ["r1", "r2"]:
            rel = record.get(key)
            if rel:
                start = rel.get("start")
                end = rel.get("end")
                rel_type = rel.get("type")
                add_node_and_link(start, None, "Node")
                add_node_and_link(end, None, "Node")
                add_node_and_link(end, None, "Node", start, rel_type)

    return {
        "graph": {
            "nodes": list(nodes.values()),
            "links": links
        }
    }
