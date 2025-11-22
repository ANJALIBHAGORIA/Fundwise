"""
vector_store_updater.py
-----------------------
Purpose:
    Update vector stores used for similarity search (VectorDB)
    based on new user behavior embeddings, feedback, or anomalies.
"""

import json
import numpy as np

class VectorStoreUpdater:
    def __init__(self, vector_db_path: str):
        """
        vector_db_path: JSON file storing user behavior embeddings
        """
        self.vector_db_path = vector_db_path
        try:
            with open(vector_db_path, 'r') as f:
                self.vector_store = json.load(f)
        except FileNotFoundError:
            self.vector_store = {}

    def update_user_vector(self, user_id: str, new_embedding: list):
        """
        Update or add a new user embedding
        Args:
            user_id: User identifier
            new_embedding: List of float numbers representing vector
        """
        self.vector_store[user_id] = new_embedding
        with open(self.vector_db_path, 'w') as f:
            json.dump(self.vector_store, f, indent=4)
        return f"Vector updated for user {user_id}"

    def get_user_vector(self, user_id: str):
        return self.vector_store.get(user_id, None)

if __name__ == "__main__":
    updater = VectorStoreUpdater('user_behaviour_embeddings.json')
    test_vector = list(np.random.rand(128))
    print(updater.update_user_vector('user_101', test_vector))
