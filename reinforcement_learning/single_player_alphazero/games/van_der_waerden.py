from .game import Game


class VanDerWaerden(Game, only_terminal_highscore=False):
    num_colors = None
    max_prog = None
    max_size = None
