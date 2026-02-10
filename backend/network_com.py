from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
user = "neo4j"
password = "dairynet"

driver = GraphDatabase.driver(uri, auth=(user, password))
'''
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        for record in result:
            print(record["test"])

test_connection()
'''
def fetch_network_data():
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m LIMIT 2000
    """
    try:
        with driver.session() as session:
            results = session.run(query)

            nodes = {}
            links = []

            for record in results:
                # Extract node and relationship details
                source_node = record["n"]
                target_node = record["m"]
                relationship = record["r"]

                # Add nodes
                source_id = source_node.id  # Use Neo4j internal ID
                target_id = target_node.id
                source_label = source_node.get("name", f"Node-{source_id}")
                target_label = target_node.get("name", f"Node-{target_id}")

                if source_id not in nodes:
                    nodes[source_id] = {"id": source_id, "label": source_label}
                if target_id not in nodes:
                    nodes[target_id] = {"id": target_id, "label": target_label}

                # Add relationships
                links.append({
                    "source": source_id,
                    "target": target_id,
                    "type": relationship.type
                })

            return {
                "nodes": list(nodes.values()),
                "links": links
            }

    except Exception as e:
        print("Error fetching network data:", e)
        raise
