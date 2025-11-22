"""
behavior_score_model.py
-----------------------
Purpose:
    Compute behavior scores for users based on profile deviations and clustering.
    Score can be used for trust scoring or anomaly detection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

class BehaviorScoreModel:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def fit_model(self, user_profiles: pd.DataFrame):
        """
        Fit IsolationForest on user features
        Args:
            user_profiles: DataFrame with numeric behavioral features
        """
        features = user_profiles.drop(columns=['user_id'])
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        self.scaler = scaler
        self.model.fit(scaled_features)
        self.user_profiles = user_profiles

    def compute_scores(self) -> pd.DataFrame:
        """
        Compute anomaly scores (-1 = anomaly, 1 = normal)
        """
        features = self.user_profiles.drop(columns=['user_id'])
        scaled_features = self.scaler.transform(features)
        scores = self.model.decision_function(scaled_features)
        self.user_profiles['behavior_score'] = scores
        return self.user_profiles[['user_id','behavior_score']]

if __name__ == "__main__":
    user_profiles = pd.DataFrame({
        'user_id':[1,2,3],
        'avg_session_duration':[0.8,0.5,0.9],
        'total_sessions':[0.9,0.4,1.0],
        'contribution_count':[0.7,0.3,0.8],
        'avg_contribution':[0.75,0.4,0.85]
    })
    model = BehaviorScoreModel()
    model.fit_model(user_profiles)
    scores = model.compute_scores()
    print(scores)
