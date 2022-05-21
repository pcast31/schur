import torch
from torch.nn.functional import cross_entropy, mse_loss

from mcts import MCTS
from replay_buffer import ReplayBuffer


class AlphaZero:
    def __call__(self, observation):
        policy, value = self.network(observation)
        return policy, value

    def __init__(
        self,
        game,
        mcts,
        n_batchs_per_game,
        n_self_play_games,
        network,
        optimizer,
        optimizer_args,
        replay_buffer,
        device,
        training_device,
    ):
        self.game = game
        self.mcts = mcts
        self.n_batchs_per_game = n_batchs_per_game
        self.n_self_play_games = n_self_play_games
        self.network = network
        self.optimizer = optimizer(network.parameters(), **optimizer_args)
        self.replay_buffer = replay_buffer
        if torch.cuda.is_available():
            default_device = torch.device('cuda:0')
        else:
            default_device = torch.device('cpu')
        if device is None:
            self.device = default_device
        else:
            self.device = torch.device(training_device)
        if training_device is None:
            self.training_device = default_device
        else:
            self.training_device = torch.device(training_device)

    @classmethod
    def from_config(cls, config, game, network):
        mcts = MCTS.from_config(config)
        n_batchs_per_game = config.n_batchs_per_game
        n_self_play_games = config.n_self_play_games
        optimizer = config.optimizer
        optimizer_args = config.optimizer_args
        replay_buffer = ReplayBuffer.from_config(config)
        device = config.device
        training_device = config.training_device
        alphazero = cls(game, mcts, n_batchs_per_game, n_self_play_games,
            network, optimizer, optimizer_args, replay_buffer, device,
            training_device)
        return alphazero

    @staticmethod
    def loss(pred_policy, pred_value, policy, value):
        return cross_entropy(pred_policy, policy) + mse_loss(pred_value, value)

    def preprocess_obs(self, observation):
        self.network.preprocess_obs(observation)

    def play_game(self):
        self.to(self.device)
        with torch.no_grad():
            game = self.mcts.play_game(self.game, self)
        return game

    def sample_batch(self):
        batch = self.replay_buffer.sample_batch()
        batch = self.network.preprocess_batch(*batch, self.training_device)
        return batch

    def to(self, device):
        self.network.to(device)

    def train(self):
        for self_play in range(self.n_self_play_games):
            game = self.play_game()
            self.replay_buffer.save_game(game)
            self.to(self.training_device)
            running_loss = 0
            for _ in range(self.n_batchs_per_game):
                running_loss += self.update_weights()
            print(f"\r[{self_play}/{self.n_self_play_games}] loss: {running_loss / self.n_batchs_per_game}")

    def update_weights(self):
        self.optimizer.zero_grad()
        loss = 0
        for observation, policy, value in self.sample_batch():
            pred_policy, pred_value = self.network(observation)
            loss += self.loss(pred_policy, pred_value, policy, value)
        loss.backward()
        self.optimizer.step()
        return loss.item()
