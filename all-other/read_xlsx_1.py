import pandas as pd
from neo4j import GraphDatabase

# Path to your Excel file
filename = "/home/melahi/code/A-mediawiki-project/copyparty/Justus-Liebig-Universität_Gießen/2025-06-23_Erfassungsformular_Q1_TH.xlsx"

# Load Excel: first two columns only
df = pd.read_excel(filename, usecols=[0, 1])

# Drop empty rows
df = df.dropna()

# Convert first two columns into dictionary {property: value}
properties = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

print("Properties to insert into Neo4j:")
print(properties)

# --- Extract Neo4j label from Genre property ---
label = properties.get("Gattung/Genre") or properties.get("Genre")
if not label:
    label = "ExcelNode"  # fallback if no genre is found

print(f"Using label: {label}")

# --- Neo4j Connection ---
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_node(tx, label, properties):
    # Dynamically build Cypher query with properties
    query = f"CREATE (n:`{label}` $props)"
    tx.run(query, props=properties)

with driver.session() as session:
    session.execute_write(create_node, label, properties)

driver.close()

print("✅ Node created in Neo4j!")
