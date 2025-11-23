"""
time_series_model.py
--------------------
Purpose:
    Build time-series models (ARIMA or Prophet) for predicting user/fund contributions.
    Used to detect anomalies based on deviation from expected patterns.
"""

import pandas as pd
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from typing import Dict

class TimeSeriesModel:
    def __init__(self, method='prophet'):
        """
        Initialize time-series model
        Args:
            method: 'prophet' or 'arima'
        """
        self.method = method
        self.model = None

    def fit(self, df: pd.DataFrame, user_id: int = None):
        """
        Fit time-series model to user/fund transactions
        Args:
            df: DataFrame with columns ['timestamp', 'amount']
            user_id: optional, for logging purposes
        """
        df_ts = df.copy()
        df_ts['timestamp'] = pd.to_datetime(df_ts['timestamp'])
        df_ts = df_ts.set_index('timestamp').resample('D').sum().fillna(0).reset_index()
        df_ts.rename(columns={'timestamp': 'ds', 'amount': 'y'}, inplace=True)

        if self.method == 'prophet':
            self.model = Prophet(daily_seasonality=True)
            self.model.fit(df_ts)
        elif self.method == 'arima':
            self.model = ARIMA(df_ts['y'], order=(5,1,0))
            self.model = self.model.fit()
        else:
            raise ValueError("Method must be 'prophet' or 'arima'")

    def predict(self, periods: int = 7) -> pd.DataFrame:
        """
        Forecast next periods
        Args:
            periods: number of future periods
        Returns:
            DataFrame with forecast values
        """
        if self.method == 'prophet':
            future = self.model.make_future_dataframe(periods=periods)
            forecast = self.model.predict(future)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        elif self.method == 'arima':
            forecast = self.model.forecast(steps=periods)
            return pd.DataFrame({'yhat': forecast})
