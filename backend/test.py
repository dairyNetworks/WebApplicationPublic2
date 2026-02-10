from neo4j import GraphDatabase

def process_graph_elements(p_node, r1, n_node, r2, related):
    # Initialize containers
    nodes = {}
    links = []

    # Helper function to add a node
    def add_node(node, node_id_prefix):
        element_id = node.element_id.split(':')[-1]  # Extract numeric part of element_id
        node_id = f"{node_id_prefix}_{element_id}"
        if node_id not in nodes:  # Avoid overwriting
            # Use the first label as the "label" for the node
            label = next(iter(node.labels)) if node.labels else "Unknown"
            nodes[node_id] = {
                "id": node_id,
                "label": label,
                **node._properties,  # Include all properties dynamically
            }
        return node_id

    # Process nodes
    p_node_id = add_node(p_node, "p")
    n_node_id = add_node(n_node, "n")
    related_id = add_node(related, "related")

    # Helper function to add a link
    def add_link(source_id, target_id, relationship):
        links.append({
            "source": source_id,
            "target": target_id,
            "type": relationship.type,  # Extract the type of the relationship
            **relationship._properties,  # Include all relationship properties dynamically
        })

    # Process relationships
    add_link(n_node_id, p_node_id, r1)
    add_link(n_node_id, related_id, r2)

    # Return final structure
    return {
        "nodes": list(nodes.values()),
        "links": links,
    }

def extract_nodes_and_links(record):
    # Extract components
    p_node = record["p"]
    print('p_node : ',p_node)
    print('p_node type : ',type(p_node))
    r1 = record["r1"]
    print('r1 : ',r1)
    print('r1 type : ',type(r1))
    n_node = record["n"]
    print('n_node : ',n_node)
    print('n_node type : ',type(n_node))
    r2 = record["r2"]
    print('r2 : ',r2)
    print('r2 type : ',type(r2))
    related_node = record["related"]
    print('related : ',related_node)
    print('related type : ',type(related_node))

    graph_data = process_graph_elements(p_node, r1, n_node, r2, related_node)
    return graph_data


def get_network_data(query, uri = "bolt://localhost:7687", user = "neo4j", password = "dairynet"):
    """
    Connect to Neo4j, execute the query, and process the result to extract graph data.
    """
    if query == "ogp":
        cypher_query = """
            MATCH (p:Policy {name: "Origin Green Programme"})-[r1]-(n)-[r2]-(related)
            WHERE type(r2) IN ["REGION", "DESIGNATION", "AFFILIATED_WITH", "POLICY_REF", "STANCE_ON_POL"]
            AND type(r1) IN ["REGION", "DESIGNATION", "AFFILIATED_WITH", "POLICY_REF", "STANCE_ON_POL"]
            RETURN p, r1, n, r2, related;
        """
    elif query == "fv":
        cypher_query = """
            MATCH (p:Policy {name: "Food Vision 2030"})-[r]-(n)
            RETURN p, r, n;
            """
    else:
        return {"nodes": [], "links": []}

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            results = session.run(cypher_query)
            graph_data_list = []
            for record in results:
                graph_data = extract_nodes_and_links(record)
                if graph_data:
                    graph_data_list.append(graph_data)
            return graph_data_list
    finally:
        driver.close()
