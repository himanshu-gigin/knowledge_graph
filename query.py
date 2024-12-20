
import generate_query 
import neo4j_client

driver = neo4j_client.connect_to_neo4j()
cypher_query = generate_query.generate_cypher_queries("What Professional Certificates includes for Sales Executive?")['query']
print(cypher_query)
results = driver.execute_query("MATCH (n) RETURN n")
print(results)