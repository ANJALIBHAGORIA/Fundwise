"""
scoring_engine.py
-----------------
Purpose:
    Compute a unified credibility score for users based on multiple signals:
    - Document verification results
    - Behavioral anomaly scores
    - Graph-based collusion or linkage anomalies
"""

import pandas as pd
from typing import Dict

class CredibilityScoringEngine:
    def __init__(self, weight_config: Dict = None):
        """
        Initialize scoring engine with optional weight configuration.
        weight_config: dict specifying weightage for different signals, e.g.,
            {'document': 0.4, 'behavior': 0.4, 'graph': 0.2}
        """
        self.weight_config = weight_config or {'document': 0.4, 'behavior': 0.4, 'graph': 0.2}

    def compute_score(self, user_signals: Dict) -> float:
        """
        Compute final credibility score for a single user
        Args:
            user_signals: dict containing:
                'document_score': float (0-1)
                'behavior_score': float (0-1)
                'graph_score': float (0-1)
        Returns:
            weighted credibility score (0-1)
        """
        score = (
            user_signals.get('document_score', 0) * self.weight_config['document'] +
            user_signals.get('behavior_score', 0) * self.weight_config['behavior'] +
            user_signals.get('graph_score', 0) * self.weight_config['graph']
        )
        return round(score, 4)

    def assign_flag(self, score: float) -> str:
        """
        Assign a credibility flag based on thresholds
        - Green: score >= 0.75
        - Yellow: 0.5 <= score < 0.75
        - Red: score < 0.5
        """
        if score >= 0.75:
            return 'Green'
        elif score >= 0.5:
            return 'Yellow'
        else:
            return 'Red'

    def score_users(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Batch compute scores for a DataFrame of users
        df should contain columns: ['user_id','document_score','behavior_score','graph_score']
        Returns:
            df with additional columns ['credibility_score','credibility_flag']
        """
        df = df.copy()
        df['credibility_score'] = df.apply(lambda x: self.compute_score({
            'document_score': x.get('document_score',0),
            'behavior_score': x.get('behavior_score',0),
            'graph_score': x.get('graph_score',0)
        }), axis=1)
        df['credibility_flag'] = df['credibility_score'].apply(self.assign_flag)
        return df

if __name__ == "__main__":
    # Example usage
    sample_df = pd.DataFrame({
        'user_id':[1,2,3],
        'document_score':[0.9,0.6,0.3],
        'behavior_score':[0.8,0.4,0.7],
        'graph_score':[0.95,0.2,0.5]
    })
    engine = CredibilityScoringEngine()
    result = engine.score_users(sample_df)
    print(result)
