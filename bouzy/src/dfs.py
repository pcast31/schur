class DFS:
    def __init__(self, k, board, max_depth):
        self.k = k
        self.board = board
        self.max_depth = max_depth
        self.fact = 0.5
        self.best_score = 0.
        self.best_assign = ([], [], [])

    def __call__(self):
        self.dfs(self.max_depth, ([], [], []))
        self.apply_best()

    def apply_best(self):
        for k, numbers in enumerate(self.best_assign):
            for num in numbers:
                self.board.add_to(k, num)

    def dfs(self, max_depth, assign):
        if max_depth == 0:
            self.dfs_update_best(assign)
            return
        terminal = True
        min_out = self.board.min_out
        for col in range(self.k):
            if self.board.can_add_to(col, min_out):
                terminal = False
                assign[col].append(min_out)
                self.board.add_to(col, min_out)
                self.dfs(max_depth - 1, assign)
                assign[col].pop()
                self.board.remove_from(col, min_out)
        if terminal:
            self.dfs_update_best(assign)

    def dfs_update_best(self, assign):
        score = self.board.evaluate(self.k - 1)
        if score > self.best_score:
            self.best_score = score
            self.best_assign = (assign[0].copy(), assign[1].copy(),
                                assign[2].copy())
