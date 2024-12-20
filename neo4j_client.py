
from neo4j import GraphDatabase

def connect_to_neo4j():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
    return driver



