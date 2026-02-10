from pathlib import Path
import json

JSON_FOLDER = Path("static/data")

FILE_MAP_LTWO = {
    "car": "carbon_fvr.json",
    #"wat": "water_fvr.json",
    "liv": "live_fvr.json"
}

def load_ltwo_json(query: str):
    file_name = FILE_MAP_LTWO.get(query)
    if not file_name:
        print(f"❌ Unknown query: {query}")
        return []

    path = JSON_FOLDER / file_name
    if not path.exists():
        print(f"❌ File not found: {path}")
        return []

    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        print(f"✅ Loaded {len(data)} LTWO records from {file_name}")
        return data

def build_ltwo_fvr_table(query: str):
    data = load_ltwo_json(query)
    table = []

    for idx, record in enumerate(data, 1):
        try:
            table.append({
                "Mission": record.get("m", {}).get("properties", {}).get("name"),
                "Mission Statement": record.get("ms", {}).get("properties", {}).get("text"),
                "Goal": record.get("g", {}).get("properties", {}).get("name"),
                "Goal Statement": record.get("gs", {}).get("properties", {}).get("text"),
                "Action": record.get("a", {}).get("properties", {}).get("name"),
                "Action Statement": record.get("as", {}).get("properties", {}).get("text")
            })
        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"✅ Total table rows: {len(table)}")
    return table


def get_carbon2_fvr():
    return build_ltwo_fvr_table("car")

def get_water2_fvr():
    return build_ltwo_fvr_table("wat")

def get_livelihood2_fvr():
    return build_ltwo_fvr_table("liv")

def get_fvr_table(query, access):
    if access != "leveltwo":
        return []

    if query in ["car", "wat", "liv"]:
        return build_ltwo_fvr_table(query)

    return []
