"""
user_profile_builder.py
-----------------------
Purpose:
    Build structured user profiles using behavioral features.
    Profiles are later used for anomaly detection and credibility scoring.
"""

import pandas as pd
from typing import Dict

class UserProfileBuilder:
    def __init__(self):
        self.profiles = pd.DataFrame()

    def build_profile(self, user_features: pd.DataFrame) -> pd.DataFrame:
        """
        Generate profile by normalizing and structuring features
        Args:
            user_features: DataFrame with raw behavioral features
        Returns:
            DataFrame with structured user profiles
        """
        df = user_features.copy()

        # Feature scaling (min-max normalization)
        numeric_cols = df.select_dtypes(include='number').columns
        for col in numeric_cols:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)
            else:
                df[col] = 0.0

        self.profiles = df
        return self.profiles

    def get_profile(self, user_id: int) -> Dict:
        """
        Retrieve a specific user profile
        """
        if self.profiles.empty:
            raise ValueError("Profiles not generated yet.")
        profile = self.profiles[self.profiles['user_id'] == user_id].to_dict(orient='records')
        return profile[0] if profile else {}

if __name__ == "__main__":
    # Example usage
    user_features = pd.DataFrame({
        'user_id':[1,2],
        'avg_session_duration':[1500, 1200],
        'total_sessions':[2,1],
        'contribution_count':[2,1],
        'avg_contribution':[150,150]
    })
    builder = UserProfileBuilder()
    profiles = builder.build_profile(user_features)
    print(profiles)
    print(builder.get_profile(1))
