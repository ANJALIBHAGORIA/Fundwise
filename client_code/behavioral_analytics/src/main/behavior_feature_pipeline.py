"""
behavior_feature_pipeline.py
-----------------------------
Purpose:
    Process raw user activity data (clicks, logins, contribution patterns) into
    numerical features suitable for anomaly detection and credibility scoring.
"""

import pandas as pd
import numpy as np
from typing import List, Dict

class BehaviorFeaturePipeline:
    def __init__(self):
        """
        Initialize pipeline. Can include config for feature engineering.
        """
        pass

    def compute_session_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute session-level features:
        - Number of logins per day
        - Average session duration
        - Inactive periods between logins
        Args:
            df: DataFrame with columns ['user_id', 'session_start', 'session_end']
        Returns:
            DataFrame with computed features
        """
        df = df.copy()
        df['session_start'] = pd.to_datetime(df['session_start'])
        df['session_end'] = pd.to_datetime(df['session_end'])
        df['session_duration'] = (df['session_end'] - df['session_start']).dt.total_seconds()
        session_features = df.groupby('user_id').agg(
            avg_session_duration=('session_duration', 'mean'),
            total_sessions=('session_duration', 'count'),
            max_session_duration=('session_duration', 'max'),
            min_session_duration=('session_duration', 'min')
        ).reset_index()
        return session_features

    def compute_behavior_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract contribution/transaction patterns as behavioral features:
        - Contribution frequency
        - Mean/variance of contribution amounts
        - Days skipped
        Args:
            df: DataFrame with columns ['user_id', 'timestamp', 'amount']
        Returns:
            DataFrame with user-level features
        """
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        agg = df.groupby('user_id').agg(
            contribution_count=('amount', 'count'),
            avg_contribution=('amount', 'mean'),
            std_contribution=('amount', 'std'),
            max_contribution=('amount', 'max'),
            min_contribution=('amount', 'min')
        ).reset_index()
        agg['std_contribution'] = agg['std_contribution'].fillna(0)
        return agg

    def generate_user_features(self, session_df: pd.DataFrame, contribution_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge session and contribution features to create a unified feature set
        Args:
            session_df: session-level features
            contribution_df: contribution-level features
        Returns:
            DataFrame with all features for modeling
        """
        df = pd.merge(session_df, contribution_df, on='user_id', how='outer')
        df.fillna(0, inplace=True)
        return df

if __name__ == "__main__":
    # Example usage
    sessions = pd.DataFrame({
        'user_id':[1,1,2],
        'session_start':['2025-11-20 09:00:00','2025-11-21 10:00:00','2025-11-20 11:00:00'],
        'session_end':['2025-11-20 09:30:00','2025-11-21 10:45:00','2025-11-20 11:20:00']
    })
    contributions = pd.DataFrame({
        'user_id':[1,1,2],
        'timestamp':['2025-11-20','2025-11-21','2025-11-20'],
        'amount':[100,200,150]
    })
    pipeline = BehaviorFeaturePipeline()
    session_features = pipeline.compute_session_features(sessions)
    contribution_features = pipeline.compute_behavior_patterns(contributions)
    user_features = pipeline.generate_user_features(session_features, contribution_features)
    print(user_features)
