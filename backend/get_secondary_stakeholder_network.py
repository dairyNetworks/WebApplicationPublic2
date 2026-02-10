import json

# -------------------------------
# Load JSON data (level two)
# -------------------------------
json_file_path = "static/data/stakeholder_map.json"

with open(json_file_path, "r", encoding="utf-8-sig") as f:
    ltwo_data = json.load(f)

# -------------------------------
# Function: get_secondary_stakeholder_network
# -------------------------------
def get_secondary_stakeholder_network(query: str, primaryStakeholder: str, access: str):
    """
    Build a network of nodes and links for a document, primary stakeholder, and related entities
    using JSON data instead of Neo4j.

    Parameters:
        query (str): Document name (e.g., "D6")
        primaryStakeholder (str): Name of the primary stakeholder
        access (str): Level of access ("leveltwo" supported)

    Returns:
        dict: {"graph": {"nodes": [...], "links": [...]}}
    """
    if access != 'leveltwo':
        return {"graph": {"nodes": [], "links": []}}

    nodes = {}
    links = []

    for record in ltwo_data:
        segments = record.get("p", {}).get("segments", [])

        doc_node = None
        author_node = None
        year_node = None
        primary_node = None
        tag_nodes = []
        secondary_nodes = []

        for segment in segments:
            start = segment.get("start", {})
            end = segment.get("end", {})
            rel = segment.get("relationship", {})

            # Document node
            if "PUBLICATION_LTWO_Document" in start.get("labels", []):
                if start.get("properties", {}).get("name") == query:
                    doc_node = start.get("properties")

            # Author
            if rel.get("type") == "PUBLICATION_LTWO_HAS_AUTHOR":
                author_node = end.get("properties")

            # Year
            if rel.get("type") == "PUBLICATION_LTWO_HAS_YEAR":
                year_node = end.get("properties")

            # Primary label
            if rel.get("type") == "PUBLICATION_LTWO_HAS_PRIMARY_LABEL":
                if end.get("properties", {}).get("name") == primaryStakeholder:
                    primary_node = end.get("properties")

            # Tag
            if rel.get("type") == "PUBLICATION_LTWO_HAS_TAG":
                tag_nodes.append(end.get("properties"))

            # Secondary label
            if rel.get("type") == "PUBLICATION_LTWO_POINTS_TO_SECONDARY":
                secondary_nodes.append(end.get("properties"))

        # Skip if any required node is missing
        if not (doc_node and author_node and year_node and primary_node):
            continue

        max_len = max(len(tag_nodes), len(secondary_nodes), 1)
        for i in range(max_len):
            tag = tag_nodes[i] if i < len(tag_nodes) else None
            secondary = secondary_nodes[i] if i < len(secondary_nodes) else None

            # Generate unique node IDs for JSON
            def node_id(prefix, name):
                return f"{prefix}_{name}"

            # Add nodes
            for n_type, n_data, tooltip_key in [
                ("Document", doc_node, "doc"),
                ("Author", author_node, "name"),
                ("Year", year_node, "value"),
                ("Primary Label", primary_node, "name"),
                ("Tag", tag, "name") if tag else (None, None, None),
                ("Secondary Label", secondary, "name") if secondary else (None, None, None)
            ]:
                if n_type and n_data:
                    nid = node_id(n_type, n_data.get("name") or n_data.get("doc") or n_data.get("value"))
                    if nid not in nodes:
                        nodes[nid] = {
                            "id": nid,
                            "label": n_data.get("name") or n_data.get("doc") or n_data.get("value"),
                            "type": n_type,
                            "tooltip": n_data.get("doc") if n_type == "Document" else n_data.get("name")
                        }

            # Add links
            if doc_node and author_node:
                links.append({"source": node_id("Document", doc_node.get("name")), 
                              "target": node_id("Author", author_node.get("name")), 
                              "type": "HAS_AUTHOR"})
            if author_node and year_node:
                links.append({"source": node_id("Author", author_node.get("name")), 
                              "target": node_id("Year", year_node.get("value")), 
                              "type": "HAS_YEAR"})
            if year_node and primary_node:
                links.append({"source": node_id("Year", year_node.get("value")), 
                              "target": node_id("Primary Label", primary_node.get("name")), 
                              "type": "HAS_PRIMARY"})
            if primary_node and tag:
                links.append({"source": node_id("Primary Label", primary_node.get("name")), 
                              "target": node_id("Tag", tag.get("name")), 
                              "type": "HAS_TAG"})
            if tag and secondary:
                links.append({"source": node_id("Tag", tag.get("name")), 
                              "target": node_id("Secondary Label", secondary.get("name")), 
                              "type": "POINTS_TO_SECONDARY"})

    print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")
    return {"graph": {"nodes": list(nodes.values()), "links": links}}
