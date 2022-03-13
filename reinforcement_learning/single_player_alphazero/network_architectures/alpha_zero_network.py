from abc import ABC, abstractmethod

from torch import nn


class AlphaZeroNetwork(nn.Module, ABC):
    @abstractmethod
    def forward(self, observation):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def preprocess_obs(observation):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def preprocess_batch(batch):
        raise NotImplementedError
