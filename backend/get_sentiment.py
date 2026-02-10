from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "dairynet"  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_carbon_sentiment(category, sentiment):
    query = """
        MATCH (carbon:CARBON_SENTIMENT_LONE_Topic {name: 'carbon'})
            -[:CARBON_SENTIMENT_LONE_HAS_LABEL]->(label:CARBON_SENTIMENT_LONE_Label)
        MATCH (label)-[:CARBON_SENTIMENT_LONE_HAS_THOUGHT]->(thought:CARBON_SENTIMENT_LONE_Thought)
        MATCH (thought)-[:CARBON_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:CARBON_SENTIMENT_LONE_Sentiment)
        MATCH (label)-[:CARBON_SENTIMENT_LONE_HAS_CATEGORY]->(category:CARBON_SENTIMENT_LONE_Category)
        WHERE category.name = $category AND sentiment.type = $sentiment
        RETURN DISTINCT
            label.name AS Label,
            thought.text AS Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Stakeholder": record["Label"],
                "Thought": record["Thought"]
            })
        return table


def get_water_sentiment(category, sentiment):
    query = """
        MATCH (water:WATER_SENTIMENT_LONE_Topic {name: 'water'})
            -[:WATER_SENTIMENT_LONE_HAS_LABEL]->(label:WATER_SENTIMENT_LONE_Label)
        MATCH (label)-[:WATER_SENTIMENT_LONE_HAS_THOUGHT]->(thought:WATER_SENTIMENT_LONE_Thought)
        MATCH (thought)-[:WATER_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:WATER_SENTIMENT_LONE_Sentiment)
        MATCH (label)-[:WATER_SENTIMENT_LONE_HAS_CATEGORY]->(category:WATER_SENTIMENT_LONE_Category)
        WHERE category.name = $category AND sentiment.type = $sentiment
        RETURN DISTINCT
            label.name AS Label,
            thought.text AS Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Stakeholder": record["Label"],
                "Thought": record["Thought"]
            })
        return table


def get_live_sentiment(category, sentiment):
    query = """
        MATCH (live:LIVE_SENTIMENT_LONE_Topic {name: 'live'})
            -[:LIVE_SENTIMENT_LONE_HAS_LABEL]->(label:LIVE_SENTIMENT_LONE_Label)
        MATCH (label)-[:LIVE_SENTIMENT_LONE_HAS_THOUGHT]->(thought:LIVE_SENTIMENT_LONE_Thought)
        MATCH (thought)-[:LIVE_SENTIMENT_LONE_HAS_SENTIMENT]->(sentiment:LIVE_SENTIMENT_LONE_Sentiment)
        MATCH (label)-[:LIVE_SENTIMENT_LONE_HAS_CATEGORY]->(category:LIVE_SENTIMENT_LONE_Category)
        WHERE category.name = $category AND sentiment.type = $sentiment
        RETURN DISTINCT
            label.name AS Label,
            thought.text AS Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Stakeholder": record["Label"],
                "Thought": record["Thought"]
            })
        return table
    
def get_carbon2_sentiment(category, sentiment):
    query = """
        MATCH (cat:CARBON_SENTIMENT_LTWO_Category {name: $category})
        -[:CARBON_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:CARBON_SENTIMENT_LTWO_Designation)
        -[:CARBON_SENTIMENT_LTWO_HAS_THOUGHT]->(thought:CARBON_SENTIMENT_LTWO_Thought)
        -[:CARBON_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:CARBON_SENTIMENT_LTWO_Sentiment {type: $sentiment})
        
        RETURN DISTINCT 
        cat.name AS Category,
        desig.name AS Designation,
        thought.text AS Thought
        ORDER BY Category, Designation, Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Category": record["Category"],
                "Designation" : record["Designation"],
                "Thought": record["Thought"]
            })
        return table


def get_water2_sentiment(category, sentiment):
    query = """
        MATCH (cat:WATER_SENTIMENT_LTWO_Category {name: $category})
        -[:WATER_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:WATER_SENTIMENT_LTWO_Designation)
        -[:WATER_SENTIMENT_LTWO_HAS_THOUGHT]->(thought:WATER_SENTIMENT_LTWO_Thought)
        -[:WATER_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:WATER_SENTIMENT_LTWO_Sentiment {type: $sentiment})
        
        RETURN DISTINCT 
        cat.name AS Category,
        desig.name AS Designation,
        thought.text AS Thought
        ORDER BY Category, Designation, Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Category": record["Category"],
                "Designation" : record["Designation"],
                "Thought": record["Thought"]
            })
        return table


def get_live2_sentiment(category, sentiment):
    query = """
        MATCH (cat:LIVE_SENTIMENT_LTWO_Category {name: $category})
        -[:LIVE_SENTIMENT_LTWO_HAS_DESIGNATION]->(desig:LIVE_SENTIMENT_LTWO_Designation)
        -[:LIVE_SENTIMENT_LTWO_HAS_THOUGHT]->(thought:LIVE_SENTIMENT_LTWO_Thought)
        -[:LIVE_SENTIMENT_LTWO_HAS_SENTIMENT]->(sentiment:LIVE_SENTIMENT_LTWO_Sentiment {type: $sentiment})
        
        RETURN DISTINCT 
        cat.name AS Category,
        desig.name AS Designation,
        thought.text AS Thought
        ORDER BY Category, Designation, Thought
    """
    
    with driver.session() as session:
        results = session.run(query, category = category, sentiment = sentiment)
        table = []
        for record in results:
            table.append({
                "Category": record["Category"],
                "Designation" : record["Designation"],
                "Thought": record["Thought"]
            })
        return table

def get_sentiment(query, category, sentiment, access):
    if query == "car" and access == 'levelone':
        return get_carbon_sentiment(category, sentiment)
    elif query == "wat" and access == 'levelone':
        return get_water_sentiment(category, sentiment)
    elif query == "liv" and access == 'levelone':
        return get_live_sentiment(category, sentiment)
    elif query == "car" and access == 'leveltwo':
        return get_carbon2_sentiment(category, sentiment)
    elif query == "wat" and access == 'leveltwo':
        return get_water2_sentiment(category, sentiment)
    elif query == "liv" and access == 'leveltwo':
        return get_live2_sentiment(category, sentiment)
    else:
        return []