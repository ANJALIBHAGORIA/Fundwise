"""
contribution_timeline_builder.py
--------------------------------
Purpose:
    Build contribution timeline data for visualization in the dashboard.
    Useful to track fund growth and identify anomalies.
"""

import pandas as pd

class ContributionTimelineBuilder:
    def __init__(self, transactions: pd.DataFrame):
        """
        transactions: DataFrame with columns ['fund_id','user_id','amount','timestamp']
        """
        self.transactions = transactions

    def build_timeline(self, fund_id: int) -> pd.DataFrame:
        """
        Returns a DataFrame aggregated by day showing cumulative contributions
        """
        fund_txns = self.transactions[self.transactions['fund_id'] == fund_id].copy()
        fund_txns['date'] = pd.to_datetime(fund_txns['timestamp']).dt.date
        daily_sum = fund_txns.groupby('date')['amount'].sum().cumsum().reset_index()
        daily_sum.rename(columns={'amount':'cumulative_contribution'}, inplace=True)
        return daily_sum

if __name__ == "__main__":
    txns = pd.DataFrame([
        {'fund_id':101,'user_id':1,'amount':200,'timestamp':'2025-11-20 10:00'},
        {'fund_id':101,'user_id':2,'amount':300,'timestamp':'2025-11-21 12:00'},
        {'fund_id':101,'user_id':1,'amount':200,'timestamp':'2025-11-22 14:00'}
    ])
    timeline_builder = ContributionTimelineBuilder(txns)
    print(timeline_builder.build_timeline(101))
