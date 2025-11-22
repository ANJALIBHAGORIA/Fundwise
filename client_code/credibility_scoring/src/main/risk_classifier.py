"""
risk_classifier.py
------------------
Purpose:
    Classify users into risk categories based on credibility score,
    to trigger additional verification or restrict fund access.
"""

from scoring_engine import CredibilityScoringEngine

class RiskClassifier:
    def __init__(self, weight_config=None):
        self.engine = CredibilityScoringEngine(weight_config)

    def classify_user(self, user_signals: dict) -> dict:
        """
        Args:
            user_signals: dict with 'document_score', 'behavior_score', 'graph_score'
        Returns:
            dict: {'credibility_score': float, 'credibility_flag': str, 'risk_level': str}
        """
        score = self.engine.compute_score(user_signals)
        flag = self.engine.assign_flag(score)
        if flag == 'Green':
            risk_level = 'Low'
        elif flag == 'Yellow':
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        return {'credibility_score': score, 'credibility_flag': flag, 'risk_level': risk_level}

    def batch_classify(self, df):
        """
        Args:
            df: DataFrame with user signals
        Returns:
            DataFrame with added 'credibility_score', 'credibility_flag', 'risk_level'
        """
        df = df.copy()
        results = df.apply(lambda row: self.classify_user({
            'document_score': row['document_score'],
            'behavior_score': row['behavior_score'],
            'graph_score': row['graph_score']
        }), axis=1)
        df['credibility_score'] = results.apply(lambda x: x['credibility_score'])
        df['credibility_flag'] = results.apply(lambda x: x['credibility_flag'])
        df['risk_level'] = results.apply(lambda x: x['risk_level'])
        return df

if __name__ == "__main__":
    import pandas as pd
    sample_users = pd.DataFrame({
        'user_id':[1,2,3],
        'document_score':[0.9,0.6,0.3],
        'behavior_score':[0.8,0.4,0.7],
        'graph_score':[0.95,0.2,0.5]
    })
    classifier = RiskClassifier()
    result = classifier.batch_classify(sample_users)
    print(result)
