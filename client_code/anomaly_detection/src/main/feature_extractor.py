"""
feature_extractor.py
--------------------
Purpose:
    Extract relevant features from transactional data for anomaly detection.
    Works on individual transactions as well as user/group aggregated features.
"""

import pandas as pd
import numpy as np
from typing import List, Dict

class FeatureExtractor:
    def __init__(self):
        """
        Initialize feature extractor. 
        Can extend to load feature configs or scaling parameters.
        """
        pass

    def basic_transaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract basic features from transactions
        Args:
            df: pandas DataFrame with columns ['user_id', 'amount', 'timestamp', 'fund_id']
        Returns:
            DataFrame with new feature columns
        """
        df = df.copy()
        # Transaction amount statistics
        df['log_amount'] = np.log1p(df['amount'])
        df['is_large_txn'] = df['amount'] > df['amount'].quantile(0.95)

        # Time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

        return df

    def user_aggregated_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate features per user
        Args:
            df: pandas DataFrame with transaction data
        Returns:
            DataFrame with user-level aggregated features
        """
        agg_df = df.groupby('user_id').agg(
            txn_count=('amount', 'count'),
            txn_sum=('amount', 'sum'),
            txn_mean=('amount', 'mean'),
            txn_std=('amount', 'std'),
            txn_max=('amount', 'max'),
            txn_min=('amount', 'min')
        ).reset_index()

        # Fill missing std with 0
        agg_df['txn_std'] = agg_df['txn_std'].fillna(0)
        return agg_df

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Full pipeline to generate all features
        """
        df_txn = self.basic_transaction_features(df)
        df_user = self.user_aggregated_features(df_txn)
        return df_user


if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame({
        'user_id': [1, 1, 2, 2],
        'amount': [100, 2000, 150, 500],
        'timestamp': ['2025-11-20 10:00:00', '2025-11-20 15:00:00',
                      '2025-11-21 12:00:00', '2025-11-21 18:00:00'],
        'fund_id': [101,101,102,102]
    })
    fe = FeatureExtractor()
    features = fe.generate_features(sample_data)
    print(features)
