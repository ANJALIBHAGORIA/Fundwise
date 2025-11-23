"""
user_event_ingestor.py
---------------------
Purpose:
    Collects and stores user-generated events from the platform,
    e.g., login, contribution, withdrawal, device changes.
"""

import pandas as pd
from datetime import datetime

class UserEventIngestor:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        try:
            self.events_df = pd.read_csv(storage_path)
        except FileNotFoundError:
            self.events_df = pd.DataFrame(columns=['event_id', 'user_id', 'event_type', 'timestamp', 'metadata'])

    def ingest_event(self, user_id: int, event_type: str, metadata: dict = None):
        new_event = {
            'event_id': len(self.events_df)+1,
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': datetime.now(),
            'metadata': metadata
        }
        self.events_df = pd.concat([self.events_df, pd.DataFrame([new_event])], ignore_index=True)
        self.events_df.to_csv(self.storage_path, index=False)
        return f"Event ingested for user {user_id}"

if __name__ == "__main__":
    ingestor = UserEventIngestor('user_events.csv')
    print(ingestor.ingest_event(101, 'login', {'ip':'192.168.1.1'}))
