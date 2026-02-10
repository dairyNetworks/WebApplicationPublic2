import json

# -------------------------------
# Load JSON data
# -------------------------------
json_file_path = "static/data/stakeholder_map.json"

with open(json_file_path, "r", encoding="utf-8-sig") as f:
    ltwo_data = json.load(f)

# -------------------------------
# Function: get_secondary_stakeholder
# -------------------------------
def get_secondary_stakeholder(query: str, primaryStakeholder: str, access: str):
    """
    Extract secondary stakeholders for a given document and primary stakeholder from JSON.

    Parameters:
        query (str): Document name (e.g., "D6")
        primaryStakeholder (str): Name of the primary stakeholder
        access (str): Level of access ("leveltwo" supported)

    Returns:
        list[dict]: List of dictionaries with the following keys:
            Document, Author, Year, Primary Stakeholder, Primary Category,
            Secondary Stakeholder, Secondary Category, Tag, Context
    """
    if access != 'leveltwo':
        return []

    table = []
    seen = set()  # for deduplication

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

        # Combine nodes into table
        if doc_node and author_node and year_node and primary_node:
            max_len = max(len(tag_nodes), len(secondary_nodes), 1)
            for i in range(max_len):
                tag = tag_nodes[i] if i < len(tag_nodes) else None
                secondary = secondary_nodes[i] if i < len(secondary_nodes) else None

                row_tuple = (
                    doc_node.get("doc"),
                    author_node.get("name"),
                    year_node.get("value"),
                    primary_node.get("name"),
                    None,
                    secondary.get("name") if secondary else None,
                    None,
                    tag.get("name") if tag else None,
                    tag.get("context") if tag else None
                )

                if row_tuple not in seen:
                    seen.add(row_tuple)
                    table.append({
                        "Document": row_tuple[0],
                        "Author": row_tuple[1],
                        "Year": row_tuple[2],
                        "Primary Stakeholder": row_tuple[3],
                        "Primary Category": row_tuple[4],
                        "Secondary Stakeholder": row_tuple[5],
                        "Secondary Category": row_tuple[6],
                        "Tag": row_tuple[7],
                        "Context": row_tuple[8]
                    })

    return table
