from pathlib import Path
import json

JSON_FOLDER = Path("static/data")  # folder containing your LTWO JSON files

def load_ltwo_json(query):
    """Load the LTWO JSON file for a given query (car/wat/liv)"""
    file_map = {
        "car": "carbon_fvr.json",
        #"wat": "water_fvr.json",
        "liv": "live_fvr.json"
    }
    file_name = file_map.get(query)
    if not file_name:
        print(f"❌ Unknown query: {query}")
        return []

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


def get_ltwo_fvr_stakeholder(query, action):
    data = load_ltwo_json(query)
    table = []

    for idx, record in enumerate(data, 1):
        try:
            if not isinstance(record, dict):
                print(f"⚠️ Skipping malformed record {idx}: {record}")
                continue

            # Only include records matching the requested action
            record_action = record.get("a", {}).get("properties", {}).get("name")
            if record_action != action:
                continue

            mission = record.get("m", {}).get("properties", {}).get("name")
            mission_statement = record.get("ms", {}).get("properties", {}).get("text")
            goal = record.get("g", {}).get("properties", {}).get("name")
            goal_statement = record.get("gs", {}).get("properties", {}).get("text")
            action_name = record_action
            action_statement = record.get("as", {}).get("properties", {}).get("text")

            # Collect all stakeholders
            stakeholders = []

            l_field = record.get("l")
            if isinstance(l_field, dict):
                name = l_field.get("properties", {}).get("name")
                if name:
                    stakeholders.append(name)
            s_field = record.get("s")
            if isinstance(s_field, dict):
                name = s_field.get("properties", {}).get("name")
                if name:
                    stakeholders.append(name)

            # If no stakeholders, keep one row with None
            if not stakeholders:
                table.append({
                    "Mission": mission,
                    "Mission Statement": mission_statement,
                    "Goal": goal,
                    "Goal Statement": goal_statement,
                    "Action": action_name,
                    "Action Statement": action_statement,
                    "Stakeholder": None
                })
            else:
                for stakeholder in stakeholders:
                    table.append({
                        "Mission": mission,
                        "Mission Statement": mission_statement,
                        "Goal": goal,
                        "Goal Statement": goal_statement,
                        "Action": action_name,
                        "Action Statement": action_statement,
                        "Stakeholder": stakeholder
                    })
        except Exception as e:
            print(f"❌ Error processing record {idx}: {e}")

    print(f"✅ Total table rows: {len(table)}")
    return table


# Wrapper function for frontend use
def get_fvr(query, action, access):
    if access != "leveltwo":
        print("⚠️ Only LTWO JSON supported in this version")
        return []

    return get_ltwo_fvr_stakeholder(query, action)
