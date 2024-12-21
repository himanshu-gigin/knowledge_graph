
import pandas as pd
import create_graph
import utils


# i have a csv file name sales_executive.csv import the data in pandas
def prepare_relationships(file_path: str):
    df = pd.read_csv(file_path)
    cleaned_df = utils.clean_dataframe(df)
    return cleaned_df



sale_executive = prepare_relationships("../data/sales_executive_final.csv")
cafe_manager = prepare_relationships("../data/cafe_manager_final.csv")
field_executive = prepare_relationships("../data/field_sale_final.csv")



def create_graph_from_dataset(dataframe):
    node1 = dataframe['NodeOne'].unique()
    node2 = dataframe[["NodeTwo", "NodeClass"]].drop_duplicates().set_index("NodeTwo").to_dict()["NodeClass"]
    print(node1, node2)
    for node in node1:
        create_graph.create_node_label('JobRole', node)
    for key, value in node2.items():
        print(f"{key}: {value}")
        create_graph.create_node_label(value,key)

create_graph_from_dataset(sale_executive)
create_graph_from_dataset(cafe_manager)
create_graph_from_dataset(field_executive)



#  #create relationship
for index, row in sale_executive.iterrows():
    print(row)
    create_graph.create_relationship('JobRole', row['NodeOne'], row['Relation'], row['NodeClass'],row['NodeTwo'])
     #create relationship
for index, row in cafe_manager.iterrows():
    create_graph.create_relationship('JobRole', row['NodeOne'], row['Relation'], row['NodeClass'],row['NodeTwo'], )
    #  create relationship
for index, row in field_executive.iterrows():
    create_graph.create_relationship('JobRole', row['NodeOne'], row['Relation'], row['NodeClass'],row['NodeTwo'] )
    