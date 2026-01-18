from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# Neo4j connection details
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "your_password"

# Cypher query to retrieve graph data
CYPHER_QUERY = """
MATCH (n)-[r]->(m)
RETURN n.name AS source, type(r) AS relationship, m.name AS target
LIMIT 100
"""

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def fetch_graph_data():
    with driver.session() as session:
        result = session.run(CYPHER_QUERY)
        return [(record["source"], record["relationship"], record["target"]) for record in result]


# Build the graph
def build_graph(data):
    G = nx.DiGraph()
    for source, rel, target in data:
        G.add_edge(source, target, label=rel)
    return G


# Visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))

    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10,
            arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Neo4j Graph Visualization")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    data = fetch_graph_data()
    G = build_graph(data)
    visualize_graph(G)
