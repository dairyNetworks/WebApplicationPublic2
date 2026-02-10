from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "dairynet"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_CARBON_SENTIMENT_L1_network(category, sentiment):
    cypher_query = """
    MATCH (carbon:CARBON_SENTIMENT_LONE_Topic {name: 'carbon'})-[:CARBON_SENTIMENT_LONE_HAS_LABEL]->(label:CARBON_SENTIMENT_LONE_Label)
    MATCH (label)-[:CARBON_SENTIMENT_LONE_HAS_CATEGORY]->(category:CARBON_SENTIMENT_LONE_Category)
    MATCH (label)-[:CARBON_SENTIMENT_LONE_HAS_THOUGHT]->(thought:CARBON_SENTIMENT_LONE_Thought)
    MATCH (thought)-[:CARBON_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:CARBON_SENTIMENT_LONE_Sentiment)
    WHERE category.name = $category AND sentiment.type = $sentiment

    RETURN DISTINCT
        id(carbon) AS id_c, carbon.name AS label_c, 'Topic' AS type_c,
        id(label) AS id_l, label.name AS label_l, 'Label' AS type_l
"""
    
    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add nodes
            for prefix, label in [('c', 'Topic'), ('l', 'Label')]:
                node_id = record[f"id_{prefix}"]
                node_label = record[f"label_{prefix}"]
                node_type = record[f"type_{prefix}"]
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node_label,
                        "type": node_type
                    }

            # Create links
            links.append({"source": record["id_c"], "target": record["id_l"], "type": "HAS_LABEL"})
            #links.append({"source": record["id_l"], "target": record["id_o"], "type": "HAS_ORGANISATION"})
            #links.append({"source": record["id_l"], "target": record["id_d"], "type": "HAS_DESIGNATION"})

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

def get_WATER_SENTIMENT_L1__network(category, sentiment):
    cypher_query = """
        MATCH (water:WATER_SENTIMENT_LONE_Topic {name: 'water'})-[:WATER_SENTIMENT_LONE_HAS_LABEL]->(label:WATER_SENTIMENT_LONE_Label)
        MATCH (label)-[:WATER_SENTIMENT_LONE_HAS_CATEGORY]->(category:WATER_SENTIMENT_LONE_Category)
        MATCH (label)-[:WATER_SENTIMENT_LONE_HAS_THOUGHT]->(thought:WATER_SENTIMENT_LONE_Thought)
        MATCH (thought)-[:WATER_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:WATER_SENTIMENT_LONE_Sentiment)
        WHERE category.name = $category AND sentiment.type = $sentiment

        RETURN DISTINCT
            id(water) AS id_c, water.name AS label_c, 'Topic' AS type_c,
            id(label) AS id_l, label.name AS label_l, 'Label' AS type_l
    """
        
    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add nodes
            for prefix, label in [('c', 'Topic'), ('l', 'Label')]:
                node_id = record[f"id_{prefix}"]
                node_label = record[f"label_{prefix}"]
                node_type = record[f"type_{prefix}"]
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node_label,
                        "type": node_type
                    }

            # Create links
            links.append({"source": record["id_c"], "target": record["id_l"], "type": "HAS_LABEL"})
            #links.append({"source": record["id_l"], "target": record["id_o"], "type": "HAS_ORGANISATION"})
            #links.append({"source": record["id_l"], "target": record["id_d"], "type": "HAS_DESIGNATION"})

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

def get_LIVE_SENTIMENT_L1__network(category, sentiment):
    cypher_query = """
    MATCH (live:LIVE_SENTIMENT_LONE_Topic {name: 'live'})-[:LIVE_SENTIMENT_LONE_HAS_LABEL]->(label:LIVE_SENTIMENT_LONE_Label)
    MATCH (label)-[:LIVE_SENTIMENT_LONE_HAS_CATEGORY]->(category:LIVE_SENTIMENT_LONE_Category)
    MATCH (label)-[:LIVE_SENTIMENT_LONE_HAS_THOUGHT]->(thought:LIVE_SENTIMENT_LONE_Thought)
    MATCH (thought)-[:LIVE_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:LIVE_SENTIMENT_LONE_Sentiment)
    WHERE category.name = $category AND sentiment.type = $sentiment

    RETURN DISTINCT
        id(live) AS id_c, live.name AS label_c, 'Topic' AS type_c,
        id(label) AS id_l, label.name AS label_l, 'Label' AS type_l
"""
    
    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add nodes
            for prefix, label in [('c', 'Topic'), ('l', 'Label')]:
                node_id = record[f"id_{prefix}"]
                node_label = record[f"label_{prefix}"]
                node_type = record[f"type_{prefix}"]
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node_label,
                        "type": node_type
                    }

            # Create links
            links.append({"source": record["id_c"], "target": record["id_l"], "type": "HAS_LABEL"})
            #links.append({"source": record["id_l"], "target": record["id_o"], "type": "HAS_ORGANISATION"})
            #links.append({"source": record["id_l"], "target": record["id_d"], "type": "HAS_DESIGNATION"})

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

def get_CARBON_SENTIMENT_L2_network(category, sentiment):
    cypher_query = """
    MATCH (CARBON:CARBON_SENTIMENT_LTWO_Topic {name: 'carbon'})
          -[:CARBON_SENTIMENT_LTWO_HAS_CATEGORY]->(cat:CARBON_SENTIMENT_LTWO_Category {name: $category})
          -[:CARBON_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:CARBON_SENTIMENT_LTWO_Designation)
          -[:CARBON_SENTIMENT_LTWO_HAS_THOUGHT]->(:CARBON_SENTIMENT_LTWO_Thought)
          -[:CARBON_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:CARBON_SENTIMENT_LTWO_Sentiment {type: $sentiment})
    RETURN DISTINCT
        id(CARBON) AS id_t, CARBON.name AS label_t, 'Topic' AS type_t,
        id(cat) AS id_c, cat.name AS label_c, 'Category' AS type_c,
        id(desig) AS id_d, desig.name AS label_d, 'Designation' AS type_d
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add Topic node
            t_id = record["id_t"]
            if t_id not in nodes:
                nodes[t_id] = {
                    "id": t_id,
                    "label": record["label_t"],
                    "fullLabel": record["label_t"],
                    "type": record["type_t"]
                }

            # Add Category node
            c_id = record["id_c"]
            if c_id not in nodes:
                nodes[c_id] = {
                    "id": c_id,
                    "label": record["label_c"],
                    "fullLabel": record["label_c"],
                    "type": record["type_c"]
                }

            # Add Designation node
            d_id = record["id_d"]
            if d_id not in nodes:
                nodes[d_id] = {
                    "id": d_id,
                    "label": record["label_d"],
                    "fullLabel": record["label_d"],
                    "type": record["type_d"]
                }

            # Add links
            links.append({
                "source": t_id,
                "target": c_id,
                "type": "CARBON_SENTIMENT_LTWO_HAS_CATEGORY"
            })
            links.append({
                "source": c_id,
                "target": d_id,
                "type": "CARBON_SENTIMENT_LTWO_HAS_DESIGNATION"
            })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching CARBON Sentiment L2 network:", e)
        raise

def get_WATER_SENTIMENT_L2_network(category, sentiment):
    cypher_query = """
    MATCH (WATER:WATER_SENTIMENT_LTWO_Topic {name: 'water'})
          -[:WATER_SENTIMENT_LTWO_HAS_CATEGORY]->(cat:WATER_SENTIMENT_LTWO_Category {name: $category})
          -[:WATER_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:WATER_SENTIMENT_LTWO_Designation)
          -[:WATER_SENTIMENT_LTWO_HAS_THOUGHT]->(:WATER_SENTIMENT_LTWO_Thought)
          -[:WATER_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:WATER_SENTIMENT_LTWO_Sentiment {type: $sentiment})
    RETURN DISTINCT
        id(WATER) AS id_t, WATER.name AS label_t, 'Topic' AS type_t,
        id(cat) AS id_c, cat.name AS label_c, 'Category' AS type_c,
        id(desig) AS id_d, desig.name AS label_d, 'Designation' AS type_d
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add Topic node
            t_id = record["id_t"]
            if t_id not in nodes:
                nodes[t_id] = {
                    "id": t_id,
                    "label": record["label_t"],
                    "fullLabel": record["label_t"],
                    "type": record["type_t"]
                }

            # Add Category node
            c_id = record["id_c"]
            if c_id not in nodes:
                nodes[c_id] = {
                    "id": c_id,
                    "label": record["label_c"],
                    "fullLabel": record["label_c"],
                    "type": record["type_c"]
                }

            # Add Designation node
            d_id = record["id_d"]
            if d_id not in nodes:
                nodes[d_id] = {
                    "id": d_id,
                    "label": record["label_d"],
                    "fullLabel": record["label_d"],
                    "type": record["type_d"]
                }

            # Add links
            links.append({
                "source": t_id,
                "target": c_id,
                "type": "WATER_SENTIMENT_LTWO_HAS_CATEGORY"
            })
            links.append({
                "source": c_id,
                "target": d_id,
                "type": "WATER_SENTIMENT_LTWO_HAS_DESIGNATION"
            })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching WATER Sentiment L2 network:", e)
        raise

def get_LIVE_SENTIMENT_L2_network(category, sentiment):
    cypher_query = """
    MATCH (LIVE:LIVE_SENTIMENT_LTWO_Topic {name: 'live'})
          -[:LIVE_SENTIMENT_LTWO_HAS_CATEGORY]->(cat:LIVE_SENTIMENT_LTWO_Category {name: $category})
          -[:LIVE_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:LIVE_SENTIMENT_LTWO_Designation)
          -[:LIVE_SENTIMENT_LTWO_HAS_THOUGHT]->(:LIVE_SENTIMENT_LTWO_Thought)
          -[:LIVE_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:LIVE_SENTIMENT_LTWO_Sentiment {type: $sentiment})
    RETURN DISTINCT
        id(LIVE) AS id_t, LIVE.name AS label_t, 'Topic' AS type_t,
        id(cat) AS id_c, cat.name AS label_c, 'Category' AS type_c,
        id(desig) AS id_d, desig.name AS label_d, 'Designation' AS type_d
    """

    session = driver.session()
    try:
        results = session.run(cypher_query, category=category, sentiment=sentiment)

        nodes = {}
        links = []

        for record in results:
            # Add Topic node
            t_id = record["id_t"]
            if t_id not in nodes:
                nodes[t_id] = {
                    "id": t_id,
                    "label": record["label_t"],
                    "fullLabel": record["label_t"],
                    "type": record["type_t"]
                }

            # Add Category node
            c_id = record["id_c"]
            if c_id not in nodes:
                nodes[c_id] = {
                    "id": c_id,
                    "label": record["label_c"],
                    "fullLabel": record["label_c"],
                    "type": record["type_c"]
                }

            # Add Designation node
            d_id = record["id_d"]
            if d_id not in nodes:
                nodes[d_id] = {
                    "id": d_id,
                    "label": record["label_d"],
                    "fullLabel": record["label_d"],
                    "type": record["type_d"]
                }

            # Add links
            links.append({
                "source": t_id,
                "target": c_id,
                "type": "LIVE_SENTIMENT_LTWO_HAS_CATEGORY"
            })
            links.append({
                "source": c_id,
                "target": d_id,
                "type": "LIVE_SENTIMENT_LTWO_HAS_DESIGNATION"
            })

        print(f"\n✅ Total nodes: {len(nodes)}, Total links: {len(links)}")

        return {
            "graph": {
                "nodes": list(nodes.values()),
                "links": links
            }
        }

    except Exception as e:
        print("❌ Error fetching LIVE Sentiment L2 network:", e)
        raise


def get_sentiment_network(query, category, sentiment,access):
    if query == "car" and access == 'levelone':
        return get_CARBON_SENTIMENT_L1_network(category, sentiment)
    elif query == "wat" and access == 'levelone':
        return get_WATER_SENTIMENT_L1__network(category, sentiment)
    elif query == "liv" and access == 'levelone':
        return get_LIVE_SENTIMENT_L1__network(category, sentiment)
    elif query == "car" and access == 'leveltwo':
        return get_CARBON_SENTIMENT_L2_network(category, sentiment)
    elif query == "wat" and access == 'leveltwo':
        return get_WATER_SENTIMENT_L2_network(category, sentiment)
    elif query == "liv" and access == 'leveltwo':
        return get_LIVE_SENTIMENT_L2_network(category, sentiment)
    else:
        return []