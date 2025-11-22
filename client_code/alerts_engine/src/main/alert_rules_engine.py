"""
alert_rules_engine.py
--------------------
Purpose:
    Core engine to define, evaluate, and trigger alerts based on user
    credibility scores, behavioral anomalies, graph-based fraud signals,
    and escrow rules.
"""

import yaml

class AlertRulesEngine:
    def __init__(self, rules_file: str):
        """
        Load alert rules from YAML config
        """
        with open(rules_file, 'r') as f:
            self.rules = yaml.safe_load(f)

    def evaluate_user(self, user_score: float, risk_category: str):
        """
        Evaluate user risk and determine alert action
        Args:
            user_score: Combined credibility score (0-1)
            risk_category: 'green', 'yellow', 'red' from scoring engine
        Returns:
            action: 'allow', 'manual_review', 'block'
        """
        rule = self.rules.get(risk_category, {})
        if user_score >= rule.get('min_score', 0):
            return rule.get('action', 'allow')
        return 'manual_review'

    def evaluate_fund(self, fund_id: int, fund_status: str, red_flag_count: int):
        """
        Evaluate pooled fund status for alerts
        Args:
            fund_status: 'pending', 'completed', 'released'
            red_flag_count: number of red-flagged users
        Returns:
            action: 'release', 'hold', 'manual_review'
        """
        if fund_status == 'completed' and red_flag_count == 0:
            return 'release'
        elif red_flag_count > 0:
            return 'manual_review'
        return 'hold'

if __name__ == "__main__":
    engine = AlertRulesEngine('alert_templates.yaml')
    action_user = engine.evaluate_user(user_score=0.7, risk_category='yellow')
    print("User action:", action_user)
    action_fund = engine.evaluate_fund(fund_id=101, fund_status='completed', red_flag_count=1)
    print("Fund action:", action_fund)
