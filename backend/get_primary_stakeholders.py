import json

# Load JSON once (keep it global or load inside the function)
with open("static/data/stakeholder_map.json", "r", encoding="utf-8-sig") as f:
    ltwo_data = json.load(f)

def get_primary_stakeholders(query: str, access: str):
    if access != 'leveltwo':
        return []

    stakeholders = set()

    for record in ltwo_data:
        segments = record.get("p", {}).get("segments", [])
        for segment in segments:
            rel = segment.get("relationship", {})
            end = segment.get("end", {})

            # Only consider primary label relationships
            if rel.get("type") != "PUBLICATION_LTWO_HAS_PRIMARY_LABEL":
                continue

            # Make sure this segment belongs to the document we want
            end_props = end.get("properties", {})
            if end_props.get("docName") != query:
                continue

            # Add primary stakeholder name
            name = end_props.get("name")
            if name:
                stakeholders.add(name)

    return sorted(stakeholders)
