import collections
import random

import numpy as np
import torch


class ReplayBuffer:
    def __init__(self, window_size, batch_size):
        self.window_size = window_size
        self.batch_size = batch_size
        self.buffer = collections.deque(maxlen=self.window_size)

    @staticmethod
    def _make_tensor_batch(arrays):
        return torch.from_numpy(np.concatenate(arrays))

    @classmethod
    def from_config(cls, config):
        window_size = config.window_size
        batch_size = config.batch_size
        replay_buffer = cls(window_size, batch_size)
        return replay_buffer

    def save_game(self, game):
        self.buffer.append(game)

    def sample_batch(self):
        games = random.choices(self.buffer, k=self.batch_size)
        batch = zip(*map(self.sample_position, games))
        observations, polcies, values = map(self._make_tensor_batch, batch)
        return observations, polcies, values

    @staticmethod
    def sample_position(game):
        index = random.randrange(len(game) - 1)
        position = game.make_image(index)
        target = game.make_target(index)
        return position, target
