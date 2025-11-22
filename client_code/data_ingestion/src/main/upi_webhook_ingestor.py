"""
upi_webhook_ingestor.py
-----------------------
Purpose:
    Receive UPI transaction webhooks from payment providers (Razorpay/NPCI sandbox)
    Parse incoming events and store them for downstream processing.
"""

import json
from typing import Dict
import pandas as pd
from datetime import datetime

class UPIWebhookIngestor:
    def __init__(self, storage_path: str):
        """
        storage_path: CSV/DB path where incoming transactions are stored
        """
        self.storage_path = storage_path
        try:
            self.df = pd.read_csv(storage_path)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['txn_id', 'user_id', 'fund_id', 'amount', 'status', 'timestamp', 'raw_payload'])

    def ingest_webhook(self, payload: Dict):
        """
        Ingest a single UPI webhook payload
        Args:
            payload: Dictionary representing webhook JSON
        """
        txn = {
            'txn_id': payload.get('txn_id'),
            'user_id': payload.get('user_id'),
            'fund_id': payload.get('fund_id'),
            'amount': payload.get('amount'),
            'status': payload.get('status'),
            'timestamp': payload.get('timestamp', datetime.now()),
            'raw_payload': json.dumps(payload)
        }
        self.df = pd.concat([self.df, pd.DataFrame([txn])], ignore_index=True)
        self.df.to_csv(self.storage_path, index=False)
        return f"Webhook ingested: {txn['txn_id']}"

if __name__ == "__main__":
    ingestor = UPIWebhookIngestor('transactions.csv')
    sample_payload = {'txn_id': 'TXN123', 'user_id': 101, 'fund_id': 201, 'amount': 500, 'status': 'SUCCESS'}
    print(ingestor.ingest_webhook(sample_payload))
