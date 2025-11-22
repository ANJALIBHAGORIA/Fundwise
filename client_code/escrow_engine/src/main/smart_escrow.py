class Escrow:
    def __init__(self):
        self.ledger = []
    def lock(self, tx):
        self.ledger.append(tx)
        return True
