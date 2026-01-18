from neo4j import GraphDatabase

# Replace with your connection details
NEO4J_URI = "bolt://localhost:7687"  # or neo4j:// if using encrypted connection
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

class Neo4jCleaner:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def delete_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

if __name__ == "__main__":
    cleaner = Neo4jCleaner(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        cleaner.delete_all()
        print("All nodes and relationships have been deleted.")
    finally:
        cleaner.close()
