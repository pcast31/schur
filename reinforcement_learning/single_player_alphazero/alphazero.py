import torch
from torch.nn.functional import cross_entropy, mse_loss

from mcts import MCTS
from replay_buffer import ReplayBuffer


class AlphaZero:
    def __init__(
        self,
        game,
        mcts,
        n_batchs_per_game,
        n_self_play_games,
        network,
        optimizer,
        replay_buffer,
        self_play_on_gpu,
        training_device,
    ):
        self.game = game
        self.mcts = mcts
        self.network = network
        self.n_batchs_per_game = config.n_batchs_per_game
        self.n_self_play_games = config.n_self_play_games
        self.optimizer = optimizer(network.parameters())
        self.replay_buffer = self.replay_buffer
        if self_play_on_gpu:
            if torch.cuda.is_available():
                self.device = torch.device('cuda:0')
            else
                raise ValueError("Impossible to play on GPU, cuda is not available.")
        else:
            self.device = torch.device('cpu')
        if training_device is None:
            if torch.cuda.is_available()
                self.training_device = torch.device('cuda:0')
            else:
                self.training_device = torch.device('cpu')
        else:
            self.training_device = torch.device(training_device)

    def __call__(self, observation):
        policy, value = self.network(observation)
        return policy, value

    @classmethod
    def from_config(cls, config, game, network):
        mcts = MCTS.from_config(config)
        n_batchs_per_game = config.n_batchs_per_game
        n_self_play_games = config.n_self_play_games
        optimizer = config.optimizer
        replay_buffer = ReplayBuffer.from_config(config)
        self_play_on_gpu = config.self_play_on_gpu
        training_device = config.training_device
        alphazero = cls(game, mcts, n_batchs_per_game, n_self_play_games, network,
            optimizer, replay_buffer, self_play_on_gpu, training_device)

    @staticmethod
    def loss(pred_policy, pred_value, policy, value):
        return cross_entropy(pred_policy, policy) + mse_loss(pred_value, value)

    def observation_to_tensor(self, observation):
        batched_observation = observation.reshape((1, *observation.shape))
        tensor_observation = torch.from_numpy()
        observation = observation.to(self.device)
        return observation

    def play_game(self):
        self.to(self.device)
        with torch.no_grad():
            game = self.mcts.play_game(self.game, self)
        return game

    def to(self, device):
        self.network.to(device)

    def train(self):
        for self_play in range(self.n_self_play_games):
            game = self.play_game()
            self.replay_buffer.save_game(game)
            self.to(self.training_device)
            running_loss = 0
            for batch in range(self.n_batchs_per_game):
                running_loss += self.update_weights()
            print(f"\r[{self_play}/{self.n_self_play_games}] loss: {loss / self.n_batchs_per_game}")

    def update_weights(self):
        observation, policy, value = map(lambda tensor: tensor.to(self.training_device),
            self.replay_buffer.sample_batch())
        self.optimizer.zero_grad()
        pred_policy, pred_value = self.network(observation)
        loss = self.loss(pred_policy, pred_value, policy, value)
        loss.backward()
        self.optimizer.step()
        return loss.item()
