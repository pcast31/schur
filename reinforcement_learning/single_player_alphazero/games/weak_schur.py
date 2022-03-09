from .game import Game


class WeakSchur(Game):
    def __init__(self, k, n):
        self.k = k
        self.n = n
