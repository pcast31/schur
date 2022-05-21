import sys

import games

game = getattr(games, sys.argv[1])
game.main()
