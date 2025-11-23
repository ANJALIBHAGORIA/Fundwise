"""
shap_explainer.py
-----------------
Purpose:
    Generate explainable AI outputs using SHAP (SHapley Additive exPlanations)
    for individual user scores, contribution anomalies, and fund risk.
    Provides transparency to moderators and users.
"""

import shap
import pandas as pd

class SHAPExplainer:
    def __init__(self, model, feature_data: pd.DataFrame):
        """
        model: Trained AI/ML model (behavioral, graph, or scoring)
        feature_data: DataFrame containing features used for model predictions
        """
        self.model = model
        self.feature_data = feature_data
        self.explainer = shap.Explainer(model.predict, feature_data)

    def explain_user(self, user_id: int, user_features: pd.Series):
        """
        Generate SHAP values for a single user
        Args:
            user_id: unique ID of user
            user_features: Series of user feature values
        Returns:
            shap_values: SHAP explanation object
        """
        shap_values = self.explainer(user_features)
        return shap_values

    def summary_plot(self, shap_values):
        """
        Display summary plot for feature importance
        """
        shap.summary_plot(shap_values, self.feature_data)

if __name__ == "__main__":
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier

    # Example model and data
    X = pd.DataFrame(np.random.rand(5, 4), columns=['feature1','feature2','feature3','feature4'])
    y = [0,1,0,1,0]
    model = RandomForestClassifier().fit(X, y)

    explainer = SHAPExplainer(model, X)
    shap_vals = explainer.explain_user(user_id=1, user_features=X.iloc[0])
    explainer.summary_plot(shap_vals)
