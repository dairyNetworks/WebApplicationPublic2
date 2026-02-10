from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "dairynet"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_table_data():
    query = """
        MATCH (m:food_vision_num_MISSION)-[:food_vision_num_HAS_GOAL]->(g:food_vision_num_GOAL)
        MATCH (g)-[:food_vision_num_HAS_ACTION]->(a:food_vision_num_ACTION)
        MATCH (a)-[:food_vision_num_INVOLVES]->(s:food_vision_num_ACTION_STAKEHOLDER)
        OPTIONAL MATCH (m)-[:food_vision_num_HAS_MISSION_STATEMENT]->(ms:food_vision_num_MISSION_STATEMENT)
        OPTIONAL MATCH (g)-[:food_vision_num_HAS_GOAL_STATEMENT]->(gs:food_vision_num_GOAL_STATEMENT)
        OPTIONAL MATCH (a)-[:food_vision_num_HAS_ACTION_STATEMENT]->(as:food_vision_num_ACTION_STATEMENT)
        RETURN 
            m.name AS Mission,
            ms.text AS Mission_Statement,
            g.name AS Goal,
            gs.text AS Goal_Statement,
            a.name AS Action,
            as.text AS Action_Statement,
            s.name AS Action_Stakeholder
    """
    with driver.session() as session:
        results = session.run(query)
        table = []
        for record in results:
            table.append({
                "Mission": record["Mission"],
                "Mission Statement": record["Mission_Statement"],
                "Goal": record["Goal"],
                "Goal Statement": record["Goal_Statement"],
                "Action": record["Action"],
                "Action Statement": record["Action_Statement"],
                "Stakeholder": record["Action_Stakeholder"]
            })
        return table

def get_network_data(query):
    session = driver.session()
    try:
        if query == "ogp":
            cypher_query = """
                MATCH (m:food_vision_num_MISSION)-[:food_vision_num_HAS_GOAL]->(g:food_vision_num_GOAL)
                MATCH (g)-[:food_vision_num_HAS_ACTION]->(a:food_vision_num_ACTION)
                MATCH (a)-[:food_vision_num_INVOLVES]->(s:food_vision_num_ACTION_STAKEHOLDER)
                RETURN 
                    id(m) AS id_m, m.name AS label_m, 'MISSION' AS type_m,
                    id(g) AS id_g, g.name AS label_g, 'GOAL' AS type_g,
                    id(a) AS id_a, a.name AS label_a, 'ACTION' AS type_a,
                    id(s) AS id_s, s.name AS label_s, 'STAKEHOLDER' AS type_s
            """
        elif query == "fv":
            cypher_query = """
                MATCH (p:Policy {name: "Food Vision 2030"})-[r]-(n)
                RETURN p, r, n
            """
        else:
            return {"graph": {"nodes": [], "links": []}, "table": []}

        results = session.run(cypher_query)

        nodes = {}
        links = []

        for record in results:
            if query == "ogp":
                # Add nodes with type
                for prefix in ['m', 'g', 'a', 's']:
                    node_id = record[f"id_{prefix}"]
                    node_label = record[f"label_{prefix}"]
                    node_type = record[f"type_{prefix}"]
                    if node_id not in nodes:
                        nodes[node_id] = {
                            "id": node_id,
                            "label": node_label,
                            "type": node_type  # 👈 Use this for coloring
                        }

                # Add edges
                links.append({"source": record["id_m"], "target": record["id_g"], "type": "HAS_GOAL"})
                links.append({"source": record["id_g"], "target": record["id_a"], "type": "HAS_ACTION"})
                links.append({"source": record["id_a"], "target": record["id_s"], "type": "INVOLVES"})

            else:
                node_ids_in_record = []
                for item in record.values():
                    if item is None:
                        continue
                    if hasattr(item, "labels"):
                        node_id = item.id
                        label = item.get("name") or item.get("text") or f"Node-{node_id}"
                        if node_id not in nodes:
                            nodes[node_id] = {
                                "id": node_id,
                                "label": label
                            }
                        node_ids_in_record.append(node_id)
                    elif hasattr(item, "type"):
                        source_id = item.start_node.id
                        target_id = item.end_node.id
                        rel_type = item.type
                        links.append({
                            "source": source_id,
                            "target": target_id,
                            "type": rel_type
                        })
                if len(node_ids_in_record) > 1 and not any(hasattr(v, "type") for v in record.values()):
                    for i in range(len(node_ids_in_record) - 1):
                        links.append({
                            "source": node_ids_in_record[i],
                            "target": node_ids_in_record[i + 1],
                            "type": "connected"
                        })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            },
            "table": []  # You can add table data here later
        }

    except Exception as e:
        print("❌ Error fetching network data:", e)
        raise