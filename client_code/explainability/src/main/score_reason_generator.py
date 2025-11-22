"""
score_reason_generator.py
------------------------
Purpose:
    Generate human-readable explanations for user/fund risk scores.
    Converts AI model outputs and anomaly detection results into
    textual descriptions for dashboards or notifications.
"""

class ScoreReasonGenerator:
    def __init__(self):
        pass

    def generate_reason(self, user_id, score, feature_impacts, graph_flag=False):
        """
        Args:
            user_id: User identifier
            score: Computed credibility or risk score
            feature_impacts: Dict of features and their contribution
            graph_flag: Boolean indicating graph-based suspicion
        Returns:
            reason_text: Readable explanation for dashboards or alerts
        """
        reason_text = f"User {user_id} has a risk score of {score:.2f}.\n"
        reason_text += "Contributing factors:\n"
        for feat, impact in feature_impacts.items():
            reason_text += f"- {feat}: {impact:+.2f}\n"
        if graph_flag:
            reason_text += "- Graph-based anomaly detected (possible collusion).\n"
        return reason_text

if __name__ == "__main__":
    feature_impacts = {'contribution_variance': 0.15, 'device_change': 0.2}
    generator = ScoreReasonGenerator()
    explanation = generator.generate_reason(user_id=101, score=0.45, feature_impacts=feature_impacts, graph_flag=True)
    print(explanation)
