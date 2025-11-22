"""
user_tag_updater.py
------------------
Purpose:
    Dynamically assign user tags (Red, Yellow, Green) based on
    combined credibility score, anomaly detection, and graph signals.
"""

class UserTagUpdater:
    def __init__(self, scoring_engine, graph_engine):
        """
        scoring_engine: Instance of CredibilityScoringEngine
        graph_engine: Instance of GNN/Graph analysis
        """
        self.scoring_engine = scoring_engine
        self.graph_engine = graph_engine

    def compute_tag(self, user_id: int):
        """
        Compute risk tag for a user
        Returns:
            tag: 'red', 'yellow', 'green'
        """
        score = self.scoring_engine.get_user_score(user_id)
        graph_flag = self.graph_engine.is_suspicious(user_id)
        
        if graph_flag or score < 0.3:
            return 'red'
        elif score < 0.7:
            return 'yellow'
        return 'green'

    def update_user_tag(self, user_db, user_id: int):
        """
        Update user tag in database
        """
        tag = self.compute_tag(user_id)
        user_db.loc[user_db['user_id']==user_id, 'tag'] = tag
        return tag

if __name__ == "__main__":
    class DummyScoring:
        def get_user_score(self, uid): return 0.5 if uid==1 else 0.8
    class DummyGraph:
        def is_suspicious(self, uid): return True if uid==1 else False

    user_db = [{'user_id':1,'tag':''}, {'user_id':2,'tag':''}]
    updater = UserTagUpdater(DummyScoring(), DummyGraph())
    print(updater.update_user_tag(user_db, 1))  # red
    print(updater.update_user_tag(user_db, 2))  # green
