from .game import Game


class VanDerWaerden(Game):
    def __init__(self, k, d, n):
        self.k = k
        self.d = d
        self.n = n
