

import neo4j_client

driver = neo4j_client.connect_to_neo4j()
cypher_query = "" # TODO: Write a Cypher query to retrieve all nodes from the graph
results = driver.execute_query("MATCH (n) RETURN n")
print(results)