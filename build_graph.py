import pandas as pd
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF
from rdflib import Graph, URIRef, Literal, RDF
import neo4j_client


# Load the CSV
csv_file = "dataset.csv"
df = pd.read_csv(csv_file)

# Define namespaces
EX = Namespace("http://example.org/")

# Create RDF graph
g = Graph()

# Helper function to sanitize strings for URIs
def sanitize_uri(value):
    return URIRef(EX[value.replace(" ", "_").replace("'", "")])

# Add triples from CSV
for index, row in df.iterrows():

    # Create URIs for subject and object
    subject = URIRef(EX[row['node1'].replace(' ', '_')])
    predicate = URIRef(EX[row['relationship'].replace(' ', '_')])
    object_ = URIRef(EX[row['node2'].replace(' ', '_')])
        
    # Add the triple to the graph
    g.add((subject, predicate, object_))
    
    # Add metadata
g.add((URIRef(EX['metadata']), 
           URIRef(EX['generated_on']), 
           Literal("2024-12-20 03:34:45")))
g.add((URIRef(EX['metadata']), 
           URIRef(EX['generated_by']), 
           Literal("himanshu-gigin")))


# Save to RDF file
g.serialize("roles.rdf", format="xml")
print("RDF file created: roles.rdf")



def execute_query(driver, query):
    with driver.session() as session:
        results = session.run(query)
        return [ result.data() for result in results ]

# Insert RDF Triples into Neo4j
def insert_rdf_to_neo4j(driver, rdf_file_path):
    g = Graph()
    g.parse(rdf_file_path, format="xml")  # Assuming RDF/XML format

    # Iterate through all triples in the RDF graph and insert them into Neo4j
    with driver.session(database='salesexecutive') as session:
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
    

    
# Path to the RDF file
rdf_file_path = "roles.rdf" 

# Connect to Neo4j
driver = neo4j_client.connect_to_neo4j()

# Insert RDF into Neo4j
insert_rdf_to_neo4j(driver, rdf_file_path)




