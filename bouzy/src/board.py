from random import random


class Board:
    TARGETS = [0, 2, 8, 23, 66, 197, 583, 1737, 5106]

    def __init__(self, k, aim=None, board=None, min_out=1):
        if aim is None:
            aim = self.TARGETS[k]
        if board is None:
            board = [bytearray(aim + 1) for _ in range(k)]
        self.k = k
        self.aim = aim
        self.board = board
        self.min_out = min_out
        self.fact = 0.5

    def __len__(self):
        return self.min_out - 1

    def add_to(self, k, num):
        self.board[k][num] = True
        self.min_out += 1

    def can_add_any(self, k, n):
        for col in range(k + 1):
            if self.can_add_to(col, n):
                return col
        return None

    def can_add_to(self, k, num):
        if num > self.aim:
            return False
        subset = self.board[k]
        for i in range(1, (num + 1) // 2):
            if subset[i] and subset[num - i]:
                return False
        return True

    def copy(self, k):
        board = [self.board[c].copy() for c in range(k + 1)]
        return Board(k + 1, self.aim, board, self.min_out)

    def evaluate(self, k):
        c_2 = 0.
        pow_2 = 0.5
        for num in range(self.min_out + 1, self.min_out + 6):
            if self.can_add_any(k, num) is not None:
                c_2 += pow_2
                pow_2 *= 0.5
        c_3 = random()
        evaluation = self.min_out + self.fact * c_2 + (1. - self.fact) * c_3
        return evaluation

    def fill_consec(self, k):
        while self.can_add_to(k, self.min_out):
            self.add_to(k, self.min_out)

    def fill_hole(self, assign):
        for k in assign:
            self.add_to(k, self.min_out)

    def remove_from(self, k, num):
        self.board[k][num] = False
        self.min_out -= 1

    def to_lists(self):
        partition = [[i for i, belongs_to in enumerate(subset) if belongs_to]
                     for subset in self.board]
        return partition

    def hole_ok(self, k, hole, assign, added):
        if len(assign) == len(hole):
            return assign
        if hole[len(assign)] > added:
            if self.can_add_to(k, self.min_out):
                self.add_to(k, self.min_out)
                assign.append(k)
                assign = self.hole_ok(k, hole, assign, added + 1)
                self.remove_from(k, self.min_out)
                return assign
            while len(assign) > added:
                assign.pop()
            return None
        for col in range(k):
            if self.can_add_to(col, self.min_out):
                self.add_to(col, self.min_out)
                assign.append(k)
                assign = self.hole_ok(k, hole, assign, added + 1)
                self.remove_from(k, self.min_out)
                if assign is not None:
                    return assign
                while len(assign) > added:
                    assign.pop()
        return None

    def update_first(self, board):
        self.board[:board.k] = board.board
        self.min_out = board.min_out
