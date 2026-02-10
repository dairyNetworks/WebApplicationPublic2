import csv

def resolve_json_file(label: str, mapping_csv_path: str) -> str:
    with open(mapping_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Labels"] == label:
                return row["Maping"]
    raise ValueError(f"No JSON mapping found for label: {label}")

import json
from pathlib import Path

def load_label_json(json_dir: str, json_filename: str) -> list:
    json_path = Path(json_dir) / json_filename
    with open(json_path, encoding="utf-8-sig") as f:
        return json.load(f)
    
def get_complete_network_table(label, query):
    topic_map = {
        "car": "carbon",
        "wat": "water",
        "liv": "live"
    }
    topic_filter = topic_map.get(query.lower(), query.lower())

    # ---- CONFIG ----
    MAPPING_CSV = "static/data/stakeholders.csv"
    JSON_DIR = "static/data"
    # ----------------

    try:
        # 1. Resolve JSON file
        json_filename = resolve_json_file(label, MAPPING_CSV)
        
        if not json_filename.lower().endswith(".json"):
            json_filename += ".json"
        # 2. Load JSON records
        records = load_label_json(JSON_DIR, json_filename)

        # 3. Output containers (unchanged)
        action_plans = {}
        food_wise = {}
        food_vision_action = {}
        food_vision_report = {}
        pub_tag = {}
        pub_sec_label = {}
        pub_sec_tag = {}
        pub_prim_label = {}
        designation = {}

        # 4. Iterate JSON records
        for rec in records:
            for key in ["l", "n1", "n2"]:
                node = rec.get(key)
                if not node:
                    continue

                props = node.get("properties", {})
                labels = node.get("labels", [])
                node_id = node.get("identity")

                # ---- Action Plans ----
                if "UG_AP_ACTIONS" in labels and props.get("topic") == topic_filter:
                    if node_id not in action_plans:
                        action_plans[node_id] = {
                            "id": node_id,
                            "shortaction": props.get("shortaction"),
                            "source": "Action Plan",
                            "name": props.get("name")
                        }

                # ---- Food Wise ----
                if "UG_FW_ACTIONS" in labels and props.get("topic") == topic_filter:
                    if node_id not in food_wise:
                        food_wise[node_id] = {
                            "id": node_id,
                            "shortaction": props.get("shortaction"),
                            "source": props.get("source"),
                            "recommendation": props.get("shortrecommendation"),
                            "name": props.get("name")
                        }

                # ---- Food Vision Action ----
                if "UG_FVA_ACTION" in labels and props.get("topic") == topic_filter:
                    if node_id not in food_vision_action:
                        food_vision_action[node_id] = {
                            "id": node_id,
                            "name": props.get("name"),
                            "source": props.get("source"),
                            "mission": props.get("mission"),
                            "goal": props.get("goal"),
                            "actionstatement": props.get("actionstatement")
                        }

                # ---- Food Vision Programme ----
                if "UG_FVR_PROGRAMME" in labels and props.get("topic") == topic_filter:
                    if node_id not in food_vision_report:
                        food_vision_report[node_id] = {
                            "id": node_id,
                            "name": props.get("name"),
                            "source": props.get("source"),
                            "mission": props.get("mission"),
                            "goal": props.get("goal"),
                            "actionstatement": props.get("actionstatement"),
                            "reportsummary": props.get("reportsummary")
                        }

                # ---- Publication Tag ----
                if "UG_PUB_TAG" in labels:
                    if node_id not in pub_tag:
                        pub_tag[node_id] = {
                            "id": node_id,
                            "name": props.get("name"),
                            "source": "Publications",
                            "context": props.get("context")
                        }

                # ---- Publication Secondary Label ----
                if "UG_PUB_SEC_LABEL" in labels:
                    if node_id not in pub_sec_label:
                        pub_sec_label[node_id] = {
                            "id": node_id,
                            "name": props.get("name")
                        }

                # ---- Publication Secondary Tag ----
                if "UG_PUB_SEC_TAG" in labels:
                    if node_id not in pub_sec_tag:
                        pub_sec_tag[node_id] = {
                            "id": node_id,
                            "name": props.get("name"),
                            "source": "Publications",
                            "context": props.get("context")
                        }

                # ---- Publication Primary Label ----
                if "UG_PUB_PRIM_LABELS" in labels:
                    if node_id not in pub_prim_label:
                        pub_prim_label[node_id] = {
                            "id": node_id,
                            "name": props.get("name")
                        }

                # ---- Sentiment Designation ----
                if "UG_SENT_DESIGNATION" in labels and props.get("topic") == topic_filter:
                    if node_id not in designation:
                        designation[node_id] = {
                            "id": node_id,
                            "name": props.get("name"),
                            "sentiment": props.get("sentiment"),
                            "thought": props.get("thought")
                        }

        # 5. Return EXACT same structure
        return {
            "Action_Plans": list(action_plans.values()),
            "Food_Wise": list(food_wise.values()),
            "Food_Vision_Actions": list(food_vision_action.values()),
            "Food_Vision_Reports": list(food_vision_report.values()),
            "Publication_Tags": list(pub_tag.values()),
            "Publication_Secondary_Labels": list(pub_sec_label.values()),
            "Publication_Secondary_Tags": list(pub_sec_tag.values()),
            "Publication_Primary_Labels": list(pub_prim_label.values()),
            "Sentiment_Designations": list(designation.values())
        }

    except Exception as e:
        print("Error in get_complete_network_table (JSON):", e)
        raise

