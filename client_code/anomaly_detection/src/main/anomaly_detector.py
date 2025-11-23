"""
anomaly_detector.py
-------------------
Purpose:
    Compute anomaly scores for transactions or users based on statistical deviation
    from predicted values or historical behavior.
"""

import pandas as pd
import numpy as np

class AnomalyDetector:
    def __init__(self, threshold: float = 3.0):
        """
        Args:
            threshold: z-score threshold for flagging anomalies
        """
        self.threshold = threshold

    def z_score_anomaly(self, df: pd.DataFrame, col: str = 'amount') -> pd.DataFrame:
        """
        Compute z-score anomaly
        Args:
            df: DataFrame with numeric column
            col: column to compute anomaly on
        Returns:
            DataFrame with new column 'anomaly_score' and 'is_anomaly'
        """
        df = df.copy()
        df['anomaly_score'] = (df[col] - df[col].mean()) / df[col].std()
        df['is_anomaly'] = df['anomaly_score'].abs() > self.threshold
        return df

    def deviation_from_forecast(self, df: pd.DataFrame, forecast_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare actual vs forecasted values to detect anomalies
        Args:
            df: actual data with 'timestamp', 'amount'
            forecast_df: predicted data with 'ds', 'yhat', 'yhat_lower', 'yhat_upper'
        Returns:
            DataFrame with anomaly flags
        """
        df = df.copy()
        forecast_df = forecast_df.set_index('ds')
        df['yhat'] = df['timestamp'].map(forecast_df['yhat'])
        df['yhat_upper'] = df['timestamp'].map(forecast_df['yhat_upper'])
        df['yhat_lower'] = df['timestamp'].map(forecast_df['yhat_lower'])
        df['is_anomaly'] = (df['amount'] > df['yhat_upper']) | (df['amount'] < df['yhat_lower'])
        return df
