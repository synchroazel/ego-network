# Building an Ego Network with Python and Neo4j

A system that builds and visualizes an Ego Network of a Twitter account, using Neo4j graph database and Neo4j for
visualization.

## Usage

Just run `build_graph.py` providing the name of the twitter user and the credentials to acces a running Neo4J instance.

```bash
python3 build_graph.py \
  -t <twitter username> \
  -u <neo4j username> \
  -w <neo4j password> \
  -h <neo4j hostname> \
  -p <neo4j port>
```
