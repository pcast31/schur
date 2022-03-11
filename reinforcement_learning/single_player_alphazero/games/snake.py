import itertools
import random
import tkinter as tk
from tkinter import messagebox

import numpy as np

from .game import Game


PRIME = 20_562_976_432_007
GENERATOR = 7_217_281_349_873


class Snake(Game):
    MAP = [[], [1, 5, 11, 12], [2, 4, 8, 12, 13], [9, 13], [2, 4], [1, 5],
        [10, 12], [0, 1, 2, 3, 4], [10, 12], [0, 1, 3, 4], [1, 3, 9, 13],
        [1, 3, 9, 13], [6, 9, 13], [4, 5, 9, 10, 11, 12, 13], []]

    def __call__(self):
        self._init_game()
        gui = SnakeGUI(self)
        gui()

    def __getitem__(self, index):
        return self.board[index]

    def __init__(self):
        super().__init__(4)
        self.board = np.empty((2, 15, 15), dtype=bool)
        self._seed = pow(GENERATOR, random.randrange(PRIME - 1), PRIME)
        self.apple = None
        self.circular_buffer = None
        self._head = None
        self._tail = None
        self.n_apples = None
        self.max_moves = 50
        self.moves_left = None

    def __setitem__(self, index, value):
        self.board[index] = value

    def _draw_map(self):
        for i, line in enumerate(self.MAP):
            for j in line:
                self[1, i, j] = 1

    def _init_game(self):
        self.board.fill(0)
        self.moves_left = self.max_moves
        self.score = 0
        self.n_apples = -4
        self.apple = (0, 0)
        self.terminal = False
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

    def get_observation(self):
        i, j = self.head
        observation = np.zeros((3, 15, 15), dtype=np.float32)
        observation[:2] = self.board
        observation[(2, *self.apple)] = 1
        observation = np.roll(observation, (7 - i, 7 - j), (1, 2))
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
            self.moves_left = self.max_moves
            self.n_apples += 1
            reward = 100
            over = False
            self.new_apple()
        else:
            self.moves_left -= 1
            if self.is_collision(new_head):
                reward = -50
                over = True
            else:
                reward = 0
                over = not self.moves_left
            del self.tail
        reward -= 1
        self.head = new_head
        return reward, over

    def new_apple(self):
        occupied = self.board.sum(axis=0)
        occupied[self.apple] = 1
        available = list(zip(*np.nonzero(occupied == 0)))
        self.apple = available[self._seed % len(available)]
        self._seed = (self._seed * GENERATOR) % PRIME

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
        reward, over = self.move_head(action)
        self.terminal = over
        return reward

    @property
    def tail(self):
        return self.circular_buffer[self._tail]

    @tail.deleter
    def tail(self):
        self[(0, *self.tail)] = False
        self._tail = (self._tail + 1) % 225


class SnakeGUI:
    KEYBINDS = {87: 0, 38: 0, 65: 1, 37: 1, 83: 2, 40: 2, 68: 3, 39: 3}
    ACTIONS_PER_SECOND = 5
    ROOT_COL = '#402d11'
    CANVAS_COL = '#454547'
    SNAKE_COL = '#17610d'
    APPLE_COL = '#a30716'
    WALL_COL = '#9da6ab'

    def __call__(self):
        self.root.after(100)
        self.render()
        self.root.mainloop()

    def __init__(self, game):
        root = tk.Tk()
        self.game = game
        self.action = 0
        self.running = False
        self.root = root
        self.side = min(root.winfo_screenwidth(), root.winfo_screenheight()) // 25
        self.canvas = tk.Canvas(root)
        self.score = tk.StringVar()
        self.score_label = tk.Label(self.root, textvariable=self.score)
        self.n_apples = tk.StringVar()
        self.n_apples_label = tk.Label(self.root, textvariable=self.n_apples)
        self.moves_left = tk.StringVar()
        self.moves_left_label = tk.Label(self.root, textvariable=self.moves_left)
        self.tiles = [[self._rounded_square(mid_x, mid_y)
            for mid_x in range(11 * self.side // 20, 15 * self.side, self.side)]
            for mid_y in range(11 * self.side // 20, 15 * self.side, self.side)]
        self._gui_settings()
        self._grid()
        self.render()

    def _change_color(self, tile, color):
        self.canvas.itemconfig(tile, fill=color)

    def _grid(self):
        self.canvas.grid(column=1, row=1, rowspan=3)
        self.score_label.grid(column=2, row=1)
        self.n_apples_label.grid(column=2, row=2)
        self.moves_left_label.grid(column=2, row=3)

    def _canvas_settings(self):
        side = 15 * self.side + self.side // 10
        self.canvas['width'] = side
        self.canvas['height'] = side
        self.canvas['bg'] = self.CANVAS_COL
        self.canvas['highlightthickness'] = 0

    def _grid_settings(self):
        self.root.grid_columnconfigure(0, weight=5)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=5)
        self.root.grid_rowconfigure(0, weight=4)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=4)

    def _gui_settings(self):
        self._root_settings()
        self._canvas_settings()
        self._label_setttings(self.score_label)
        self._label_setttings(self.n_apples_label)
        self._label_setttings(self.moves_left_label)
        self._grid_settings()

    def _label_setttings(self, label):
        label['bg'] = self.ROOT_COL
        label['font'] = ('Times', self.side, 'bold')
        label['fg'] = 'white'

    def _root_settings(self):
        self.root.title("Snake")
        self.root['bg'] = self.ROOT_COL
        self.root.state('zoomed')
        self.root.wm_attributes("-topmost", 1)
        self.root.focus_force()
        self.root.bind_all('<KeyPress>', self.on_keypress)

    def _rounded_square(self, mid_x, mid_y):
        side = 19 * self.side // 20
        left = mid_x - side // 2
        top = mid_y - side // 2
        right = mid_x + side // 2
        bottom = mid_y + side // 2
        radius = side // 6
        points = (left + radius, top, left + radius, top, right - radius, top,
            right - radius, top, right, top, right, top + radius, right,
            top + radius, right, bottom - radius, right, bottom - radius, right,
            bottom, right - radius, bottom, right - radius, bottom,
            left + radius, bottom, left + radius, bottom, left, bottom, left,
            bottom - radius, left, bottom - radius, left, top + radius, left,
            top + radius, left, top)
        rounded_square = self.canvas.create_polygon(points, width=0, fill='', smooth=True)
        return rounded_square

    def clear_board(self):
        for tile in itertools.chain(*self.tiles):
            self._change_color(tile, '')

    def draw_board(self):
        for i, line in enumerate(self.tiles):
            for j, tile in enumerate(line):
                if self.game[0, i, j]:
                    self._change_color(tile, self.SNAKE_COL)
                elif self.game[1, i, j]:
                    self._change_color(tile, self.WALL_COL)
        i, j = self.game.apple
        tile = self.tiles[i][j]
        self._change_color(tile, self.APPLE_COL)

    def game_over(self):
        title = "Game Over"
        message = "Game over.\nPlay again?"
        messagebox.askyesno(title=title, message=message)
        self.root.destroy()

    def on_keypress(self, event):
        try:
            action = self.KEYBINDS[event.keycode]
            if action == self.action or (action + self.action) % 2:
                self.action = action
        except KeyError:
            pass
        if not self.running:
            self.running = True
            self.step()

    def render(self):
        self.clear_board()
        self.draw_board()
        self.update_vars()

    def step(self):
        self.game.apply(self.action)
        self.render()
        if self.game.terminal:
            self.game_over()
        else:
            self.root.after(int(1000 / self.ACTIONS_PER_SECOND), self.step)

    def update_vars(self):
        self.score.set(f"Score\n{self.game.score}")
        self.n_apples.set(f"Apples\n{self.game.n_apples}")
        self.moves_left.set(f"Remaining Moves\n{self.game.moves_left}")
        if self.game.moves_left <= 10:
            self.moves_left_label['fg'] = 'red'
        else:
            self.moves_left_label['fg'] = 'white'


def main():
    Snake()()
