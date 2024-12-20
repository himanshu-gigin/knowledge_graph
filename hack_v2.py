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

# Add Instances and Data
# JobRole Instances
sales_executive = URIRef(EX.SalesExecutive)
g.add((sales_executive, RDF.type, EX.JobRole))
g.add((sales_executive, EX.name, Literal("Sales Executive")))

# Skill Instances
crm_skill = URIRef(EX.CRM)
negotiation_skill = URIRef(EX.Negotiation)

g.add((crm_skill, RDF.type, EX.Skill))
g.add((crm_skill, EX.name, Literal("Customer Relationship Management")))

g.add((negotiation_skill, RDF.type, EX.Skill))
g.add((negotiation_skill, EX.name, Literal("Negotiation Skills")))

# Link JobRole to Skills
g.add((sales_executive, EX.requiresSkill, crm_skill))
g.add((sales_executive, EX.requiresSkill, negotiation_skill))

# Qualification Instances
business_admin_degree = URIRef(EX.BusinessAdminDegree)
sales_certification = URIRef(EX.SalesCertification)

g.add((business_admin_degree, RDF.type, EX.Qualification))
g.add((business_admin_degree, EX.name, Literal("Degree in Business Administration")))

g.add((sales_certification, RDF.type, EX.Qualification))
g.add((sales_certification, EX.name, Literal("Professional Certification in Sales")))

# Serialize RDF graph to Turtle format
g.serialize("roles_v2.rdf", format="turtle")
print(g.serialize(format="turtle"))






auth_data = {'uri': 'bolt://localhost:7687',
             'database':"salesexecutivessss",
             'user':"neo4j",
             'pwd':AURA_DB_PWD}

config = Neo4jStoreConfig(auth_data=auth_data,
                          custom_prefixes="hack",
                          handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
                          batching=True)

neo4j_aura = Graph(store=Neo4jStore(config=config))
neo4j_aura.parse('roles_v2.rdf', format="turtle")
neo4j_aura.close(True)




# # Insert RDF Triples into Neo4j
# def insert_rdf_to_neo4j(driver):
#     from rdflib.namespace import RDF, RDFS

#     g = Graph()
#     g.parse('roles_v2.rdf', format="turtle")  # Assuming Turtle format

#     def sanitize(value):
#         """Replace invalid characters for Neo4j and ensure it starts with a letter."""
#         sanitized = value.replace('#', '_').replace('/', '_').replace(':', '_').replace('-', '_')
        
#         # Ensure the sanitized string starts with a letter
#         if sanitized[0].isdigit():
#             sanitized = 'n_' + sanitized  # Prefix with 'n_' if it starts with a number
        
#         return sanitized

#     # Iterate through all triples in the RDF graph and insert them into Neo4j
#     with driver.session(database='salesexecutivessss') as session:
#         for subj, pred, obj in g:
#             subj_uri = sanitize(f"{subj.split('/')[-1]}")
#             pred_uri = sanitize(f"{pred.split('/')[-1]}")
#             obj_uri = sanitize(str(obj.split('/')[-1]))

#             if pred == RDF.type:
#                 # Handle rdf:type to assign labels
#                 label = sanitize(f"{obj.split('/')[-1]}")
#                 query = f"""
#                 MERGE (node:Resource {{uri: '{subj_uri}'}})
#                 SET node:{label}
#                 """
#                 session.run(query)
#                 print(f"Assigned Label: {label} to Node: {subj_uri}")
#             else:
#                 # Handle other triples
#                 query = f"""
#                 MERGE (subject:Resource {{uri: '{subj_uri}'}})
#                 MERGE (object:Resource {{uri: '{obj_uri}'}})
#                 MERGE (subject)-[:{pred_uri.upper()}]->(object)
#                 """
#                 session.run(query)
#                 print(f"Inserted Triple: ({subj_uri}, {pred_uri}, {obj_uri})")


# insert_rdf_to_neo4j(driver)


# # Connect to Neo4j and insert RDF data
# driver = neo4j_client.connect_to_neo4j()
