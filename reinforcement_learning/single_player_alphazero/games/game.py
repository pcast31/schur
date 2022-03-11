import numpy as np


class Game:
    def __call__(self):
        raise NotImplementedError

    def __init__(self, num_actions):
        self.score = None
        self._terminal = None
        self.num_actions = num_actions
        self.history = []
        self.observations = []
        self.values = []
        self.visit_counts = []

    def __len__(self):
        return len(self.history)

    def apply(self, action, record=False):
        reward = self.step(action)
        self.score += reward
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
        value

    def step(self, action):
        raise NotImplementedError

    def store_search_statistics(self, node):
        value = node.value
        visit_counts = [0 for _ in range(self.action_space)]
        for action, child in node.children.values():
            visit_counts[action] = child.visit_count / node.visit_count
        self.values.append(value)
        self.visit_counts.append(np.array(visit_counts, dtype=np.float32))

    @property
    def terminal(self):
        if self._terminal is None:
            return not self.legal_actions()
        return self._terminal

    @terminal.setter
    def terminal(self, value):
        self._terminal = value
