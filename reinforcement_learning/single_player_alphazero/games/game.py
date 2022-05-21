from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):
    num_actions = None
    only_terminal_highscore = None
    highscore = None
    best_game = None
    subtypes = None

    def __init__(self):
        self.score = None
        self._terminal = False
        self.initial_state = None
        self.history = []
        self.observations = []
        self.values = []
        self.rewards = []
        self.visit_counts = []

    def __init_subclass__(cls, num_actions=None, only_terminal_highscore=True):
        super().__init_subclass__(cls)
        cls.num_actions = num_actions
        cls.only_terminal_highscore = only_terminal_highscore
        cls.highscore = -np.inf
        cls.best_game = None
        cls.subtypes = {}

    def __len__(self):
        return len(self.history)

    def apply(self, action, record=False):
        if record:
            observation = self.get_observation(copy=True)
            self.history.append(action)
            self.observations.append(observation)
        reward, over = self.step(action)
        self.terminal = over
        self.score += reward
        if (over or not self.only_terminal_highscore) and self.score > self.highscore:
            self.update_highscore(self.score, self.initial_state, self.history)
        observation = self.get_observation()
        return reward, observation

    @abstractmethod
    def clone(self):
        raise NotImplementedError

    @abstractmethod
    def get_observation(self, copy=False):
        raise NotImplementedError

    @abstractmethod
    def legal_actions(self):
        raise NotImplementedError

    def make_image(self, index=None):
        if index is None:
            return self.get_observation()
        return self.history[index]

    def make_target(self, index, td_steps, discount):
        if td_steps is None:
            bootstrap_index = len(self)
        else:
            bootstrap_index = index + td_steps
        if bootstrap_index < len(self):
            value = self.values[bootstrap_index]
        else:
            value = 0
        for reward in reversed(self.rewards[index: bootstrap_index + 1]):
            value = discount * value + reward
        policy = self.visit_counts[index]
        return policy, value

    @abstractmethod
    def step(self, action):
        raise NotImplementedError

    def store_search_statistics(self, node):
        reward = node.reward
        value = node.value
        visit_counts = [0 for _ in range(self.num_actions)]
        for action, child in node.children.values():
            visit_counts[action] = child.visit_count / node.visit_count
        visit_counts = np.array(visit_counts, dtype=np.float32)
        self.rewards.append(reward)
        self.values.append(value)
        self.visit_counts.append(visit_counts)

    @property
    def terminal(self):
        return self._terminal or not self.legal_actions()

    @terminal.setter
    def terminal(self, value):
        self._terminal = value

    @classmethod
    def update_highscore(cls, score, initial_state, history):
        history = history.copy()
        best_game = (initial_state, history)
        cls.highscore = score
        cls.best_game = best_game

    @classmethod
    def with_parameters(cls, num_actions=None, **kwargs):
        key = frozenset(kwargs.items())
        try:
            param_game = cls.subtypes[key]
        except KeyError:
            class_name = f"Parametric{cls.__name__}"
            param_game = type(class_name, (cls,), kwargs)
            if cls.num_actions is None:
                if num_actions is None:
                    try:
                        num_actions = kwargs['n_colors']
                    except KeyError as undefined_num_actions:
                        message = "num_actions is not defined. Define it either directly or through n_colors."
                        raise ValueError(message) from undefined_num_actions
                param_game.num_actions = num_actions
                cls.subtypes[key] = param_game
        return param_game
