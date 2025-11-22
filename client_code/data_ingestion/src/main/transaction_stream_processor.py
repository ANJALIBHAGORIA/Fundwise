"""
transaction_stream_processor.py
-------------------------------
Purpose:
    Continuously process ingested transactions for feature extraction,
    anomaly detection, and scoring.
"""

import pandas as pd
from anomaly_detection.feature_extractor import FeatureExtractor
from anomaly_detection.anomaly_detector import AnomalyDetector

class TransactionStreamProcessor:
    def __init__(self, txn_path: str):
        self.txn_path = txn_path
        self.txn_df = pd.read_csv(txn_path)
        self.feature_extractor = FeatureExtractor()
        self.anomaly_detector = AnomalyDetector()

    def process_transactions(self):
        """
        Compute features and anomaly scores for all new transactions
        """
        features = self.feature_extractor.extract_features(self.txn_df)
        self.txn_df['anomaly_score'] = self.anomaly_detector.compute_scores(features)
        self.txn_df.to_csv(self.txn_path, index=False)
        return self.txn_df[['txn_id','user_id','fund_id','anomaly_score']]

if __name__ == "__main__":
    processor = TransactionStreamProcessor('transactions.csv')
    print(processor.process_transactions())
