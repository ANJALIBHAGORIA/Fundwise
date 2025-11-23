"""
smart_escrow.py
---------------
Purpose:
    Handles escrow logic for pooled funds, enforcing fund release rules
    based on fund completion, user risk, and alerts.
    Integrates with credibility scoring and anomaly detection for decision-making.
"""

from datetime import datetime
import pandas as pd

class SmartEscrow:
    def __init__(self, fund_ledger: pd.DataFrame):
        """
        fund_ledger: DataFrame with columns
            ['fund_id', 'target_amount', 'current_amount', 'status', 'goal_date']
        """
        self.ledger = fund_ledger

    def check_fund_status(self, fund_id: int) -> str:
        """
        Returns current status of a fund:
            - 'pending' if goal not reached
            - 'completed' if target_amount reached
            - 'released' if funds already transferred
        """
        fund = self.ledger[self.ledger['fund_id'] == fund_id].iloc[0]
        if fund['status'] == 'released':
            return 'released'
        elif fund['current_amount'] >= fund['target_amount']:
            return 'completed'
        else:
            return 'pending'

    def release_funds(self, fund_id: int) -> bool:
        """
        Releases funds if conditions are met:
        - Fund completed
        - No red-flagged users in the pool
        - Optional: Time-based check for deadlines
        Returns True if released, False otherwise
        """
        fund = self.ledger[self.ledger['fund_id'] == fund_id].iloc[0]
        status = self.check_fund_status(fund_id)
        if status != 'completed':
            print(f"Fund {fund_id} not yet completed")
            return False
        
        # Here we could integrate with alerts / risk level checks
        # For now, simulate release
        self.ledger.loc[self.ledger['fund_id'] == fund_id, 'status'] = 'released'
        print(f"Funds for {fund_id} released!")
        return True

    def update_contribution(self, fund_id: int, amount: float):
        """
        Update ledger when a new contribution is made
        """
        self.ledger.loc[self.ledger['fund_id'] == fund_id, 'current_amount'] += amount

if __name__ == "__main__":
    # Sample ledger
    ledger = pd.DataFrame({
        'fund_id':[101,102],
        'target_amount':[1000,500],
        'current_amount':[500,500],
        'status':['pending','pending'],
        'goal_date':[datetime(2025,11,30), datetime(2025,12,5)]
    })
    escrow = SmartEscrow(ledger)
    escrow.update_contribution(101, 600)
    print(escrow.ledger)
    escrow.release_funds(101)
