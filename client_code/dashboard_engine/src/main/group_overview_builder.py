"""
group_overview_builder.py
------------------------
Purpose:
    Build a summarized overview of each pooled fund group for the dashboard.
    Includes total contributions, user tags, fund status, and alerts.
"""

import pandas as pd

class GroupOverviewBuilder:
    def __init__(self, fund_db: pd.DataFrame, user_db: pd.DataFrame, alerts_db: pd.DataFrame):
        """
        fund_db: DataFrame with fund_id, target_amount, current_amount, status
        user_db: DataFrame with user_id, tag
        alerts_db: DataFrame with fund_id, alert_message, timestamp
        """
        self.fund_db = fund_db
        self.user_db = user_db
        self.alerts_db = alerts_db

    def build_overview(self, fund_id: int) -> dict:
        """
        Returns a dictionary summarizing fund info for the UI
        """
        fund = self.fund_db[self.fund_db['fund_id'] == fund_id].iloc[0]
        users_in_fund = self.user_db[self.user_db['fund_id'] == fund_id]
        alerts = self.alerts_db[self.alerts_db['fund_id'] == fund_id]

        tag_counts = users_in_fund['tag'].value_counts().to_dict()
        overview = {
            'fund_id': fund_id,
            'target_amount': fund['target_amount'],
            'current_amount': fund['current_amount'],
            'status': fund['status'],
            'user_tags': tag_counts,
            'alerts': alerts.to_dict(orient='records')
        }
        return overview

if __name__ == "__main__":
    fund_db = pd.DataFrame([
        {'fund_id':101,'target_amount':1000,'current_amount':700,'status':'pending'},
        {'fund_id':102,'target_amount':500,'current_amount':500,'status':'completed'}
    ])
    user_db = pd.DataFrame([
        {'user_id':1,'fund_id':101,'tag':'red'},
        {'user_id':2,'fund_id':101,'tag':'green'},
        {'user_id':3,'fund_id':102,'tag':'green'}
    ])
    alerts_db = pd.DataFrame([
        {'fund_id':101,'alert_message':'Suspicious activity detected','timestamp':'2025-11-23'}
    ])
    builder = GroupOverviewBuilder(fund_db, user_db, alerts_db)
    print(builder.build_overview(101))
