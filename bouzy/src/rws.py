from board import Board
from dfs import DFS
from utils import is_weakly_sum_free_partition
from time import time


class RWS:
    HOLES = {'0': (), '1': (1,), '2': (2,), '12': (1, 2), '13': (1, 3),
             '14': (1, 4), '23': (2, 3)}

    def __init__(self, k, aim=None, holes=None):
        if holes is None:
            holes = list(self.HOLES.keys())
        self.k = k
        self.board = Board(k, aim)
        self.partition = None
        self.holes = [self.HOLES[hole] for hole in holes]

    def __call__(self):
        start = time()
        self.rws(self.k - 1)
        end = time()
        print(end - start)
        partition = self.board.to_lists()
        assert is_weakly_sum_free_partition(partition)
        self.partition = partition
        return partition

    def __len__(self):
        return len(self.board)

    def dfs(self, k):
        DFS(k + 1, self.board, self.board.TARGETS[k + 1])()

    def matching_holes(self, k):
        matching_holes = []
        for hole in self.holes:
            assign = self.board.hole_ok(k, hole, [], 0)
            if assign is not None:
                matching_holes.append(assign)
        return matching_holes

    def rws(self, k):
        if k <= 2:
            self.dfs(k)
            return
        self.rws(k - 1)
        best_score = 0
        best_board = None
        matching_holes = self.matching_holes(k)
        for assign in matching_holes:
            board = self.board.copy(k)
            self.board.fill_hole(assign)
            self.board.fill_consec(k)
            self.rws(k - 1)
            score = self.board.evaluate(k)
            if best_score < score:
                best_score = score
                best_board = self.board.copy(k)
            self.board.update_first(board)
        self.board.update_first(best_board)
