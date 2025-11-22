"""
visualize_graph.py
------------------
Purpose:
    Provide visualization functions for graph analysis, collusion clusters,
    and suspicious user connections.
"""

import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(graph, suspicious_users=None):
    pos = nx.spring_layout(graph)
    colors = []
    for node in graph.nodes():
        if suspicious_users and node in suspicious_users:
            colors.append('red')
        elif graph.nodes[node].get('type')=='fund':
            colors.append('blue')
        else:
            colors.append('green')
    nx.draw(graph, pos, with_labels=True, node_color=colors, node_size=800, font_size=10)
    plt.show()

if __name__ == "__main__":
    from graph_builder import GraphBuilder
    import pandas as pd
    users = pd.DataFrame({'user_id':[1,2,3]})
    funds = pd.DataFrame({'fund_id':[101]})
    contributions = pd.DataFrame({'user_id':[1,2,3],'fund_id':[101,101,101],'amount':[100,200,150],'timestamp':['2025-11-20']*3})
    builder = GraphBuilder()
    builder.add_users(users)
    builder.add_funds(funds)
    builder.add_edges(contributions)
    graph = builder.get_graph()
    plot_graph(graph, suspicious_users=[1,2])
