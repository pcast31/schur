from .game import Game


class Schur(Game, only_terminal_highscore=False):
    num_colors = None
    max_size = None
