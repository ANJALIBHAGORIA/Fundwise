"""
graph_builder.py
----------------
Purpose:
    Build user-fund relationship graphs using NetworkX.
    These graphs are later used for collusion detection, fraud detection,
    and credibility scoring.
"""

import networkx as nx
import pandas as pd

class GraphBuilder:
    def __init__(self):
        """
        Initializes an empty undirected graph
        """
        self.graph = nx.Graph()

    def add_users(self, user_df: pd.DataFrame):
        """
        Add users as nodes
        Args:
            user_df: DataFrame with columns ['user_id', 'attributes...']
        """
        for _, row in user_df.iterrows():
            self.graph.add_node(row['user_id'], **row.to_dict())

    def add_funds(self, fund_df: pd.DataFrame):
        """
        Add funds as nodes
        Args:
            fund_df: DataFrame with columns ['fund_id', 'goal', 'target_amount']
        """
        for _, row in fund_df.iterrows():
            self.graph.add_node(row['fund_id'], **row.to_dict(), type='fund')

    def add_edges(self, contributions_df: pd.DataFrame):
        """
        Add edges representing user contributions to funds
        Args:
            contributions_df: DataFrame with columns ['user_id','fund_id','amount','timestamp']
        """
        for _, row in contributions_df.iterrows():
            self.graph.add_edge(row['user_id'], row['fund_id'], amount=row['amount'], timestamp=row['timestamp'])

    def get_graph(self) -> nx.Graph:
        return self.graph

if __name__ == "__main__":
    users = pd.DataFrame({'user_id':[1,2]})
    funds = pd.DataFrame({'fund_id':[101,102], 'goal':['wedding','education'], 'target_amount':[5000,3000]})
    contributions = pd.DataFrame({'user_id':[1,2,1],'fund_id':[101,101,102],'amount':[100,200,50],'timestamp':['2025-11-20','2025-11-20','2025-11-21']})
    builder = GraphBuilder()
    builder.add_users(users)
    builder.add_funds(funds)
    builder.add_edges(contributions)
    graph = builder.get_graph()
    print(graph.nodes(data=True))
    print(graph.edges(data=True))
