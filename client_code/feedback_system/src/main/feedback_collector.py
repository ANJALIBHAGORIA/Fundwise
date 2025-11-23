"""
feedback_collector.py
--------------------
Purpose:
    Collect feedback from moderators, users, or automated systems
    regarding flagged transactions, user credibility scores, or fund anomalies.
    Feedback can be positive, negative, or neutral.
"""

import pandas as pd
from datetime import datetime

class FeedbackCollector:
    def __init__(self, feedback_db_path: str):
        """
        feedback_db_path: CSV or database path to store collected feedback
        """
        self.feedback_db_path = feedback_db_path
        try:
            self.feedback_df = pd.read_csv(feedback_db_path)
        except FileNotFoundError:
            self.feedback_df = pd.DataFrame(columns=['timestamp','user_id','fund_id','feedback_type','comments'])

    def submit_feedback(self, user_id: int, fund_id: int, feedback_type: str, comments: str = ""):
        """
        Args:
            user_id: User ID that feedback is about
            fund_id: Fund ID related to the feedback
            feedback_type: 'positive', 'negative', 'neutral'
            comments: Optional text notes
        """
        new_entry = {
            'timestamp': datetime.now(),
            'user_id': user_id,
            'fund_id': fund_id,
            'feedback_type': feedback_type,
            'comments': comments
        }
        self.feedback_df = pd.concat([self.feedback_df, pd.DataFrame([new_entry])], ignore_index=True)
        self.feedback_df.to_csv(self.feedback_db_path, index=False)
        return "Feedback submitted successfully."

if __name__ == "__main__":
    collector = FeedbackCollector('feedback_loop.csv')
    print(collector.submit_feedback(user_id=101, fund_id=201, feedback_type='negative', comments='Suspected collusion.'))
