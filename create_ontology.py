from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
import neo4j_client
from rdflib_neo4j import Neo4jStoreConfig, Neo4jStore,HANDLE_VOCAB_URI_STRATEGY
from rdflib import Graph



# Define namespaces
EX = Namespace("http://example.org/")
SCHEMA = Namespace("http://schema.org/")




# Create RDF Graph
g = Graph()

# Define Classes
g.add((EX.JobRole, RDF.type, RDFS.Class))
g.add((EX.Qualification, RDF.type, RDFS.Class))
g.add((EX.Skill, RDF.type, RDFS.Class))

# Define Properties
g.add((EX.requiresSkill, RDF.type, RDF.Property))
g.add((EX.requiresSkill, RDFS.domain, EX.JobRole))
g.add((EX.requiresSkill, RDFS.range, EX.Skill))

g.add((EX.name, RDF.type, RDF.Property))
g.add((EX.name, RDFS.domain, SCHEMA.Thing))
g.add((EX.name, RDFS.range, RDFS.Literal))


g.serialize("rdf_class.rdf", format="turtle")
print(g.serialize(format="turtle"))




# Insert RDF Triples into Neo4j
def insert_rdf_to_neo4j(driver):
    g = Graph()
    g.parse('rdf_class.rdf', format="turtle")  # Assuming RDF/XML format

    # Iterate through all triples in the RDF graph and insert them into Neo4j
    with driver.session(database='abcd') as session:
        for subj, pred, obj in g:
            # Create nodes and relationships in Neo4j
            subj_uri = f"{subj.split('/')[-1]}"
            pred_uri = f"{pred.split('/')[-1]}"
            obj_value = str(obj.split('/')[-1])

            # Construct the Cypher query for inserting RDF triples
            query = f"""
        MERGE (subject:Resource {{uri: '{subj_uri}'}})
        MERGE (predicate:Property {{uri: '{pred_uri}'}})
        MERGE (object:Resource {{uri: '{obj_value}'}})
        MERGE (subject)-[:HAS_PROPERTY]->(predicate)
        MERGE (predicate)-[:HAS_OBJECT]->(object)
        """
            session.run(query)
            print(f"Inserted Triple: ({subj_uri}, {pred_uri}, {obj_value})")
    

driver = neo4j_client.connect_to_neo4j()
insert_rdf_to_neo4j(driver)







# from neo4j import GraphDatabase
# import neo4j_client
# # Neo4j connection details
# NEO4J_URI = "bolt://localhost:7687"  # Adjust based on your Neo4j instance
# USERNAME = "neo4j"
# PASSWORD = "12345678"  # Replace with your Neo4j password

# # Neo4j Handler
# class Neo4jHandler:
#     def __init__(self):
#         self.driver = neo4j_client.driver

#     def close(self):
#         self.driver.close()

#     def execute_query(self, query, parameters=None):
#         with self.driver.session(database="abcd") as session:
#             return session.write_transaction(lambda tx: tx.run(query, parameters).data())

# # Initialize Neo4j handler
# neo4j_handler = Neo4jHandler(NEO4J_URI, USERNAME, PASSWORD)

# # Step 1: Create Indexes
# create_indexes_queries = [
#     "CREATE INDEX FOR (n:JobRole) ON (n.name)",
#     "CREATE INDEX FOR (n:Qualification) ON (n.name)",
#     "CREATE INDEX FOR (n:Skills) ON (n.name)"
# ]

# for query in create_indexes_queries:
#     neo4j_handler.execute_query(query)

# print("Indexes created successfully!")

# # Step 2: Insert Ontology Classes
# insert_ontology_classes_queries = [
#     "CREATE (:Person {name: 'Ontology_Class_Person'})",
#     "CREATE (:Organization {name: 'Ontology_Class_Organization'})",
#     "CREATE (:Event {name: 'Ontology_Class_Event'})"
# ]

# for query in insert_ontology_classes_queries:
#     neo4j_handler.execute_query(query)

# print("Ontology classes inserted successfully!")

# # Step 3: Insert Data and Relationships
# insert_data_queries = [
#     # Insert real-world Person nodes
#     "CREATE (:Person {name: 'Alice', age: 30})",
#     "CREATE (:Person {name: 'Bob', age: 25})",

#     # Insert Organization nodes
#     "CREATE (:Organization {name: 'Google', industry: 'Tech'})",
#     "CREATE (:Organization {name: 'Microsoft', industry: 'Tech'})",

#     # Insert Event nodes
#     "CREATE (:Event {name: 'GraphConnect Conference', date: '2024-10-10'})",

#     # Create relationships
#     """
#     MATCH (p:Person {name: 'Alice'}), (o:Organization {name: 'Google'})
#     CREATE (p)-[:WORKS_FOR]->(o)
#     """,
#     """
#     MATCH (p:Person {name: 'Alice'}), (e:Event {name: 'GraphConnect Conference'})
#     CREATE (p)-[:ATTENDS]->(e)
#     """
# ]

# for query in insert_data_queries:
#     neo4j_handler.execute_query(query)

# print("Data and relationships inserted successfully!")

# # Close the Neo4j connection
# neo4j_handler.close()
