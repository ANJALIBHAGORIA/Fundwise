"""
retraining_trigger.py
--------------------
Purpose:
    Monitor feedback and automatically trigger retraining
    of AI models when enough new feedback is received.
"""

import pandas as pd
import os
from datetime import datetime, timedelta

class RetrainingTrigger:
    def __init__(self, feedback_db_path: str, retrain_threshold: int = 10):
        """
        feedback_db_path: Path to feedback CSV
        retrain_threshold: Minimum number of new feedback entries to trigger retraining
        """
        self.feedback_db_path = feedback_db_path
        self.retrain_threshold = retrain_threshold
        self.last_retrain_time = datetime.min

    def check_trigger(self):
        """
        Returns True if retraining should be triggered
        """
        feedback_df = pd.read_csv(self.feedback_db_path)
        new_feedback = feedback_df[pd.to_datetime(feedback_df['timestamp']) > self.last_retrain_time]
        if len(new_feedback) >= self.retrain_threshold:
            return True
        return False

    def update_retrain_time(self):
        self.last_retrain_time = datetime.now()
        print(f"Retrain timestamp updated: {self.last_retrain_time}")

if __name__ == "__main__":
    trigger = RetrainingTrigger('feedback_loop.csv', retrain_threshold=3)
    if trigger.check_trigger():
        print("Triggering model retraining...")
        trigger.update_retrain_time()
    else:
        print("No retraining needed at this time.")
