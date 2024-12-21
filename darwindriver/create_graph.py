from typing import List
from neo4j import GraphDatabase
from fastapi import FastAPI
app = FastAPI()
from fastapi import FastAPI, UploadFile
import pandas as pd
import random
import os
import create_graph
import utils
from fastapi.middleware.cors import CORSMiddleware




# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


query_mapping = {
    "What is the required experience for the job role Cafe Lead Manager?": (
        'MATCH (r:JobRole)-[:requiresExperience]->(exp:YearOfExperience) '
        'WHERE r.name = "CafeLeadManager" '
        'RETURN DISTINCT r.name AS RoleName, exp.name AS RequiredExperience'
    ),
    "What is the qualification required for Restaurant Manager?": (
        'MATCH (r:JobRole)-[:requiresEducation]->(q:Qualification) '
        'WHERE r.name = "RestaurantManager" '
        'RETURN DISTINCT r.name AS RoleName, q.name AS RequiredQualification'
    ),
    "What additional salary benefits you gets in role Sales Executive?":(
        'MATCH (r:JobRole)-[:salaryBenefit]->(c:Compensation) '
        'WHERE r.name = "SalesExecutive" '
        'RETURN DISTINCT r.name AS RoleName, c.name AS CompensationDetails'
    ),
    "hello":(
        'MATCH (n:YearOfExperience)-[r:hasExperienceFor]->(m:JobRole) '
        'WHERE n.name = "1YearsExperience" '
        'RETURN DISTINCT n.name AS YearOfExperience ,m.name AS JobRole'
    )
}

# I have 1 year of experience in sales in local stores in my hometown in Ranchi, i am looking for some job in City, what role i should apply for?

def connect_to_neo4j():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
    return driver


# @app.get("/execute_query")
# def execute_query(query:str):
#     driver = connect_to_neo4j()
#     print(query)
#     with driver.session(database="hack") as session:
#         session.run(query)


@app.get("/execute_query")
def execute_query(query: str):
    driver = connect_to_neo4j()
    print(query)
    if(query in query_mapping):
        query = query_mapping[query]
    try:
        with driver.session(database="hack") as session:
            # Execute the query and fetch the results
            results = session.run(query)
            # Convert results to a list of dictionaries
            response = [record.data() for record in results]
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.close()



@app.post("/create_indexes")
def create_indexes(nodes: List[str]):
    for node in nodes:
        print(f'Creating index for {node}')
        query = f'CREATE INDEX {node} IF NOT EXISTS FOR (n:{node}) ON (n.{node})'
        return execute_query(query)



@app.post("/create_class_as_node")
def create_class_as_node(CLASSNAMES:List[str]):
    for node in CLASSNAMES:
        print(f'Creating class as node for {node}')
        query = f'CREATE (:{node} {{name: "{node}"}})'
        return execute_query(query)


@app.post("/create_node_label")
def create_node_label(classNode: str, node_name: str):
    query = f'CREATE (:{classNode} {{name: "{node_name}"}})'
    print(f"Creating node for {classNode}")
    return execute_query(query)



@app.post("/create_relationship")
def create_relationship(class1: str, node1_name: str, relationship: str, class2: str, node2_name: str):
    try:
        query = (
             f'MATCH (p:{class1} {{name: "{node1_name}"}}) '
    f'MATCH (o:{class2} {{name: "{node2_name}"}}) '
    f'CREATE (p)-[:{relationship}]->(o)'
        )
        print(query, "query")
        print(f"Creating relationship for {node1_name} with {node2_name} as {relationship}")
        return execute_query(query)
    except Exception as e:
        print(e)



@app.post("/enhanched/knowledge_graph")
async def enhanced_knowledge_graph(file: UploadFile):
    try:
        # save file to local
        file_location = f"temp_{file.filename}-{random.randint(1, 1000)}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # read the file
        df = pd.read_csv(file_location)
        cleaned_df = utils.clean_dataframe(df)
        # create node labels
        node1 = df[["NodeOne", "ClassForNodeOne"]].drop_duplicates().set_index("NodeOne").to_dict()["ClassForNodeOne"]
        node2 = df[["NodeTwo", "ClassForNodeTwo"]].drop_duplicates().set_index("NodeTwo").to_dict()["ClassForNodeTwo"]
        for key, value in node1.items():
            create_graph.create_node_label(value,key)
        for key, value in node2.items():
            create_graph.create_node_label(value,key)
        
        # create relationships
        for index, row in df.iterrows():
            create_graph.create_relationship(row['ClassForNodeOne'], row['NodeOne'], row['Relation'], row['ClassForNodeTwo'], row['NodeTwo'])

    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        # Clean up the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)





# create_indexes(["JobRole",
# "Skills" ,
# "Qualification",
# "YearOfExperience",
# "Industry",
# "CompanyType",
# "GeographicalLocation",
# "EducationalInstitution",
# "Proficiency",
# "Assets",
# 'Compensation',
# "WorkType",
# "WorkShift",
# "Gender"])



# create_class_as_node(["JobRole",
# "Skills" ,
# "Qualification",
# "YearOfExperience",
# "Industry",
# "CompanyType",
# "GeographicalLocation",
# "EducationalInstitution",
# "Proficiency",
# "Assets",
# 'Compensation',
# "WorkType",
# "WorkShift",
# "Gender"])


# create_node_label('JobRole', 'Sales Executive')
# create_node_label('Skills', 'CRM')
# create_relationship("JobRole", "SalesExecutive", "requiresSkill",  "Skills", "CRM")
# create_relationship("JobRole", "FieldSalesExecutive", "requiresSkill",  "Skills", "CRMUsage")