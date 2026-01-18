import re
import pandas as pd
from neo4j import GraphDatabase

# Path to your Excel file
filename = "/home/melahi/code/A-mediawiki-project/copyparty/Justus-Liebig-Universität_Gießen/2025-06-23_Erfassungsformular_Q1_TH.xlsx"

# Load Excel: first two columns only
df = pd.read_excel(filename, usecols=[0, 1])

# Drop rows where the property-name (first column) is missing
df = df.dropna(subset=[df.columns[0]])

# Convert first two columns into dictionary {property: value}
properties = {}
for k, v in zip(df.iloc[:, 0], df.iloc[:, 1]):
    if pd.isna(k):
        continue
    key = str(k).strip()
    if key == "":
        continue
    properties[key] = v

# --- Set Feldname to "GOOD" ---
properties["Feldname"] = "GOOD"

print("Properties to insert into Neo4j (Feldname set to 'GOOD'):")
print(properties)

# --- Extract first value from Genre/Gattung ---
genre_value = properties.get("Gattung/Genre") or properties.get("Genre")
if isinstance(genre_value, str) and "," in genre_value:
    genre_value = genre_value.split(",")[0].strip()  # take first value only

# Fallback if no genre found
if not genre_value or pd.isna(genre_value):
    label = "ExcelNode"
else:
    # sanitize for Neo4j label
    label_safe = re.sub(r"\W+", "_", str(genre_value).strip())  # replace non-word chars with _
    if re.match(r"^\d", label_safe):
        label_safe = "Label_" + label_safe
    label = label_safe if label_safe else "ExcelNode"

print(f"Using label: {label!r}")

# --- Neo4j Connection ---
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_node(tx, label, properties):
    query = f"CREATE (n:`{label}` $props)"
    tx.run(query, props=properties)

with driver.session() as session:
    session.execute_write(create_node, label, properties)

driver.close()

print("✅ Node created in Neo4j!")
