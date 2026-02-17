import networkx as nx
from typing import List, Dict

class ContextGraph:

    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_node(self, node_id: str, node_type: str, **attributes):

        self.graph.add_node(
            node_id,
            type=node_type,
            **attributes
        )

    def add_edge(self, source: str, target: str, relation: str):

        self.graph.add_edge(
            source,
            target,
            relation=relation
        )

    def node_exists(self, node_id: str) -> bool:

        return self.graph.has_node(node_id)

    def get_user_context_subgraph(self, user_id: str) -> Dict:
        """
        Retrieve 2-hop neighborhood around user
        """

        if not self.graph.has_node(user_id):
            return {"nodes": {}, "edges": []}

        neighbors = list(
            nx.single_source_shortest_path_length(
                self.graph,
                user_id,
                cutoff=2
            ).keys()
        )

        subgraph = self.graph.subgraph(neighbors)

        context_data = {

            "nodes": dict(subgraph.nodes(data=True)),

            "edges": [
                {
                    "source": u,
                    "target": v,
                    "relation": data.get("relation")
                }
                for u, v, data in subgraph.edges(data=True)
            ]
        }

        return context_data

    def debug_print(self):

        print("\nNodes:")
        print(list(self.graph.nodes(data=True)))

        print("\nEdges:")
        print(list(self.graph.edges(data=True)))
