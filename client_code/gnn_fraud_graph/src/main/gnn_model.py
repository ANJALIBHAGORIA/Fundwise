"""
gnn_model.py
------------
Purpose:
    Use a Graph Neural Network (PyTorch Geometric or DGL) to detect suspicious
    behavior based on graph embeddings. Produces graph_score for each user.
"""

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

class GNNFraudDetector(nn.Module):
    def __init__(self, input_dim, hidden_dim=16, output_dim=1):
        super(GNNFraudDetector, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, edge_index):
        """
        x: node features tensor [num_nodes, input_dim]
        edge_index: adjacency list tensor [2, num_edges]
        """
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return self.sigmoid(x)

# Example usage:
if __name__ == "__main__":
    # Simulate small graph
    x = torch.rand((5, 4))  # 5 nodes, 4 features
    edge_index = torch.tensor([[0,1,2,3,4,0],[1,0,3,2,0,4]], dtype=torch.long)
    model = GNNFraudDetector(input_dim=4)
    out = model(x, edge_index)
    print(out)
