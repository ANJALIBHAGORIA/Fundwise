"""
data_cleaner.py
----------------
Utility class for cleaning and preprocessing DataFrames.

Features:
- Missing value imputation
- Outlier removal using Z-score
- Safe type-aware operations
- Works even when DataFrame has non-numeric columns
"""

import pandas as pd
import numpy as np
from typing import Optional
from utils.logger import get_logger

logger = get_logger("DataCleaner")


class DataCleaner:
    """
    Utility class for cleaning DataFrames.
    """

    @staticmethod
    def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        """
        Fill missing values in a DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame
            strategy (str): "mean", "median", "zero", "ffill", "bfill"

        Returns:
            pd.DataFrame: Clean DataFrame with imputed values
        """

        if df is None or df.empty:
            logger.warning("fill_missing: Received empty DataFrame.")
            return df

        df = df.copy()
        numeric_cols = df.select_dtypes(include="number").columns

        try:
            if strategy == "mean":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            elif strategy == "median":
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            elif strategy == "zero":
                df[numeric_cols] = df[numeric_cols].fillna(0)
            elif strategy in ("ffill", "bfill"):
                df = df.fillna(method=strategy)
            else:
                logger.error(f"Invalid fill strategy: {strategy}")
        except Exception as e:
            logger.error(f"Error in fill_missing: {e}")

        return df

    @staticmethod
    def remove_outliers(
        df: pd.DataFrame, z_thresh: float = 3.0
    ) -> pd.DataFrame:
        """
        Remove outliers using Z-score thresholding.

        Args:
            df (pd.DataFrame): Input DataFrame
            z_thresh (float): Z-score threshold

        Returns:
            pd.DataFrame: DataFrame with outliers removed
        """

        if df is None or df.empty:
            logger.warning("remove_outliers: Received empty DataFrame.")
            return df

        df = df.copy()
        numeric_cols = df.select_dtypes(include="number")

        if numeric_cols.empty:
            logger.info("remove_outliers: No numeric columns found. Skipping.")
            return df

        try:
            from scipy.stats import zscore
            z_scores = numeric_cols.apply(zscore)

            # keep rows where ALL z-scores are within threshold
            mask = (abs(z_scores) < z_thresh).all(axis=1)

            cleaned_df = df[mask]

            logger.info(
                f"Outlier removal: Removed {len(df) - len(cleaned_df)} rows "
                f"(threshold={z_thresh})"
            )

            return cleaned_df

        except Exception as e:
            logger.error(f"remove_outliers error: {e}")
            return df

    @staticmethod
    def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
        """
        Trim whitespace from all string columns.
        """

        df = df.copy()
        str_cols = df.select_dtypes(include=["object", "string"]).columns

        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()

        return df

    @staticmethod
    def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete cleaning pipeline:
        - Trim whitespace
        - Fill missing values (mean)
        - Remove outliers (z=3)

        Returns:
            pd.DataFrame
        """

        df = DataCleaner.trim_whitespace(df)
        df = DataCleaner.fill_missing(df, strategy="mean")
        df = DataCleaner.remove_outliers(df, z_thresh=3)

        return df
