import collections
import random


class ReplayBuffer:
    def __init__(self, window_size, batch_size, td_steps, discount):
        self.window_size = window_size
        self.batch_size = batch_size
        self.td_steps = td_steps
        self.discount = discount
        self.buffer = collections.deque()
        self.games_length = collections.deque()

    @classmethod
    def from_config(cls, config):
        window_size = config.window_size
        batch_size = config.batch_size
        td_steps = config.td_steps
        discount = config.discount
        replay_buffer = cls(window_size, batch_size, td_steps, discount)
        return replay_buffer

    def save_game(self, game):
        self.buffer.append(game)
        self.games_length.append(len(game))
        if len(self.buffer) == self.window_size + 1:
            self.buffer.popleft()
            self.games_length.popleft()

    def sample_batch(self):
        games = random.choices(self.buffer, self.games_length, k=self.batch_size)
        batch = zip(*map(self.sample_position, games))
        observations, policies, values = map(list, batch)
        return observations, policies, values

    def sample_position(self, game):
        index = random.randrange(len(game) - 1)
        observation = game.make_image(index, self.td_steps, self.discount)
        target = game.make_target(index)
        return (observation, *target)
