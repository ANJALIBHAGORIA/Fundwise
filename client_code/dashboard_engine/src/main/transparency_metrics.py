"""
transparency_metrics.py
----------------------
Purpose:
    Compute transparency and fairness metrics for each pooled fund
    to promote trust among users and display on the dashboard.
"""

import pandas as pd

class TransparencyMetrics:
    def __init__(self, fund_db: pd.DataFrame, user_db: pd.DataFrame, transactions: pd.DataFrame):
        self.fund_db = fund_db
        self.user_db = user_db
        self.transactions = transactions

    def compute_metrics(self, fund_id: int) -> dict:
        """
        Returns transparency metrics such as:
            - number of contributors
            - average contribution
            - red/yellow/green user ratios
            - anomaly rate (optional)
        """
        fund_txns = self.transactions[self.transactions['fund_id']==fund_id]
        users = self.user_db[self.user_db['fund_id']==fund_id]
        tag_counts = users['tag'].value_counts(normalize=True).to_dict()
        
        metrics = {
            'num_contributors': len(users),
            'avg_contribution': fund_txns['amount'].mean(),
            'user_tag_ratios': tag_counts,
            'total_amount': fund_txns['amount'].sum()
        }
        return metrics

if __name__ == "__main__":
    fund_db = pd.DataFrame([{'fund_id':101,'target_amount':1000,'current_amount':700,'status':'pending'}])
    user_db = pd.DataFrame([
        {'user_id':1,'fund_id':101,'tag':'red'},
        {'user_id':2,'fund_id':101,'tag':'green'}
    ])
    transactions = pd.DataFrame([
        {'fund_id':101,'user_id':1,'amount':200,'timestamp':'2025-11-20'},
        {'fund_id':101,'user_id':2,'amount':500,'timestamp':'2025-11-21'}
    ])
    metrics = TransparencyMetrics(fund_db, user_db, transactions)
    print(metrics.compute_metrics(101))
