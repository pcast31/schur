from .game import Game


class WeakSchur(Game, only_terminal_highscore=False):
    num_colors = None
    max_size = None
