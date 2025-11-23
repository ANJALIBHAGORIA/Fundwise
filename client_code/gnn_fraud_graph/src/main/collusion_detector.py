"""
collusion_detector.py
---------------------
Purpose:
    Detect suspicious groups or collusion clusters in the user-fund graph.
    Uses heuristics and community detection to flag synthetic/fake pools.
"""

import networkx as nx
from networkx.algorithms import community

class CollusionDetector:
    def __init__(self, graph):
        self.graph = graph

    def detect_highly_connected_users(self, min_connections=3):
        """
        Identify users connected to multiple funds suspiciously
        Args:
            min_connections: threshold of funds connected
        Returns:
            List of suspicious user_ids
        """
        suspicious = []
        for node in self.graph.nodes:
            if self.graph.nodes[node].get('type') != 'fund':
                if len([n for n in self.graph.neighbors(node) if self.graph.nodes[n].get('type')=='fund']) >= min_connections:
                    suspicious.append(node)
        return suspicious

    def detect_collusion_clusters(self):
        """
        Detect tightly connected clusters using greedy modularity communities
        Returns:
            List of sets: each set is a community of nodes
        """
        communities = list(community.greedy_modularity_communities(self.graph))
        # Filter communities with only users
        user_clusters = [set(c) for c in communities if all(self.graph.nodes[n].get('type','user')!='fund' for n in c)]
        return user_clusters

if __name__ == "__main__":
    from graph_builder import GraphBuilder
    import pandas as pd
    # Sample data
    users = pd.DataFrame({'user_id':[1,2,3,4]})
    funds = pd.DataFrame({'fund_id':[101,102]})
    contributions = pd.DataFrame({'user_id':[1,2,3,4,1],'fund_id':[101,101,101,102,102],'amount':[100,200,50,150,100],'timestamp':['2025-11-20']*5})
    builder = GraphBuilder()
    builder.add_users(users)
    builder.add_funds(funds)
    builder.add_edges(contributions)
    graph = builder.get_graph()
    
    detector = CollusionDetector(graph)
    print("Suspicious users:", detector.detect_highly_connected_users())
    print("Collusion clusters:", detector.detect_collusion_clusters())
