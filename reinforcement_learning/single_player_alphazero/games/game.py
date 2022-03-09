class Game:
    def __call__(self):
        raise NotImplementedError

    def __init__(self, action_space):
        self.action_space = action_space
        self.history = []
        self.observations = []
        self.values = []
        self.visit_counts = []

    def __len__(self):
        return len(self.history)

    def apply(self, action, record=False):
        reward = self.step(action)
        observation = self.get_observation()
        if record:
            self.history.append(action)
            self.observations.append(observation.copy())
        return reward, observation

    def copy(self):
        raise NotImplementedError

    def get_observation(self):
        raise NotImplementedError

    def legal_actions(self):
        raise NotImplementedError

    def make_image(self, index=None):
        if index is None:
            return self.get_observation()
        return self.history[index]

    def make_target(self, index):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def store_search_statistics(self, node):
        value = node.value
        visit_counts = [0 for _ in range(self.action_space)]
        for action, child in node.children.values():
            visits_counts[action] = child.visit_count / node.visit_count
        self.values.append(value)
        self.visit_counts.append(np.array(visit_counts, dtype=np.float32))

    def terminal(self):
        return not self.legal_actions()
