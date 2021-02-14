from board import Board
from utils import is_weakly_sum_free_partition


class CoreRWS:
    def __init__(self, k, aim=None):
        self.k = k
        self.board = Board(k, aim)
        self.partition = None

    def __call__(self):
        self.core_rws(self.k - 1)
        partition = self.board.to_lists()
        assert is_weakly_sum_free_partition(partition)
        self.partition = partition
        return partition

    def __len__(self):
        return len(self.board)

    def core_rws(self, k):
        if k == 0:
            self.board.fill_consec(0)
            return
        self.core_rws(k - 1)
        self.board.fill_consec(k)
        self.core_rws(k - 1)
