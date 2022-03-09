import random

import numpy as np

from .game import Game


class Snake(Game):
    map = [[], [4, 11, 12], [2, 3, 4, 12, 13], [4, 13], [], [9, 11], [],
        [0, 1, 2, 3, 4, 9, 11, 14], [], [0, 1, 3, 4, 14], [1, 3], [1, 3, 6, 10],
        [6, 10], [6, 10], [6, 7, 8, 9, 10]]

    def __getitem__(self, index):
        return self.board[index]

    def __init__(self):
        super().__init__(4)
        self.board = np.empty((2, 15, 15), dtype=bool)
        self.apple = None
        self.circular_buffer = None
        self._head = None
        self._tail = None
        self.score = None
        self.max_moves = 50
        self.moves_left = None
        self.reset()

    def __setitem__(self, index, value):
        self.board[index] = value

    def _draw_map(self):
        for i, line in enumerate(self.map):
            for j in line:
                self[1, i, j] = 1

    def _init_game(self):
        self.board.fill(0)
        self.moves_left = self.max_moves
        self.score = 0
        self.apple = (0, 0)
        self._draw_map()
        self._init_snake()

    def _init_snake(self):
        self._head = -1
        self._tail = 0
        self.circular_buffer = [None for _ in range(224)] + [(11, 7)]
        self.move_head(0, True)
        self.move_head(0, True)
        self.move_head(0, True)
        self.move_head(0, True)

    def after_action(self, action, pos=None):
        if pos is None:
            i, j = self.head
        else:
            i, j = pos
        if action == 0:
            return (i - 1) % 15, j
        if action == 1:
            return i, (j - 1) % 15
        if action == 2:
            return (i + 1) % 15, j
        if action == 3:
            return i, (j + 1) % 15
        raise ValueError(f"Invalid action {action}.")

    def make_image(self):
        i, j = self.head
        observation = np.zeros((3, 15, 15), dtype=np.float32)
        observation[:2] = np.roll(self.board, (7 - i, 7 - j), (1, 2))
        observation[(2, *self.apple)] = 1
        return observation

    @property
    def head(self):
        return self.circular_buffer[self._head]

    @head.setter
    def head(self, value):
        self._head = (self._head + 1) % 225
        self.circular_buffer[self._head] = value
        self[(0, *self.head)] = True

    def is_collision(self, pos):
        if pos == self.tail:
            return False
        return self[(0, *pos)] or self[(1, *pos)]

    def is_legal(self, action):
        return not self.is_collision(self.after_action(action))

    def legal_actions(self):
        return list(filter(self.is_legal, range(4)))

    def move_head(self, action, override_apple=False):
        new_head = self.after_action(action)
        if override_apple or new_head == self.apple:
            collision = False
            self.moves_left = self.max_moves
            self.score += 1
            reward = 100
            over = False
            self.new_apple()
        else:
            collision = self.is_collision(new_head)
            self.moves_left -= 1
            if collision:
                reward = None
                over = True
            else:
                reward = -1
                over = not self.moves_left
            del self.tail
        self.head = new_head
        if not self.legal_actions():
            over = True
            reward = -25 - self.moves_left
        return reward, over, collision

    def new_apple(self):
        occupied = self.board.sum(axis=0)
        occupied[self.apple] = 1
        available = list(zip(*np.nonzero(occupied == 0)))
        self.apple = random.choice(available)

    def render(self):
        for i in range(15):
            for j in range(15):
                if self[0, i, j]:
                    print('X', end='')
                elif self[1, i, j]:
                    print('#', end='')
                elif (i, j) == self.apple:
                    print('O', end='')
                else:
                    print(' ', end='')
            print()

    def step(self, action):
        return self.move_head(action)[0]

    @property
    def tail(self):
        return self.circular_buffer[self._tail]

    @tail.deleter
    def tail(self):
        self[(0, *self.tail)] = False
        self._tail = (self._tail + 1) % 225


if __name__ == '__main__':
    game = Snake()
    game()
