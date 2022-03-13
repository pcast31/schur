import math

import numpy as np


class Node:
    def __getitem__(self, key):
        return self.children[key]

    def __init__(self, prior):
        self.prior = prior
        self.reward = None
        self.visit_count = 0
        self.value_sum = 0
        self.children = None
        self.game = None

    def __len__(self):
        return len(self.children)

    def __setitem__(self, key, value):
        self.children[key] = value

    def actions(self):
        return self.children.keys()

    def add_noise(self, noise, expl_frac):
        self.prior = self.prior * (1 - expl_frac) + noise * expl_frac

    def add_value(self, value):
        self.visit_count += 1
        self.value_sum += value

    def expand(self, game, reward, legal_actions, policy_logits):
        self.game = game
        self.reward = reward
        self.children = {}
        actions_logits = np.exp(policy_logits[legal_actions])
        policy = actions_logits / actions_logits.sum()
        for action, prior in zip(legal_actions, policy):
            self[action] = Node(prior)

    def expanded(self):
        return bool(self.children)

    def select_action(self, temperature):
        actions, children = map(list, zip(*self.children.items()))
        visit_counts = (child.visit_count for child in children)
        distrib = np.fromiter(visit_counts, dtype=np.float32)
        if temperature == 0:
            action = actions[np.argmax(distrib)]
        elif temperature == np.inf:
            action = np.random.choice(actions)
        else:
            distrib **= 1 / temperature
            distrib /= distrib.sum()
            action = np.random.choice(actions, p=distrib)
        return action

    def select_child(self, ucb_score):
        key = lambda action_child: ucb_score(action_child[1])
        action, child = max(self.children.items(), key=key)
        return action, child

    def terminal(self):
        return self.children == {}

    @property
    def value(self):
        if self.visit_count:
            return self.value_sum / self.visit_count
        return 0


class MCTS:
    def __init__(
        self,
        num_simulations,
        pb_c_base,
        pb_c_init,
        discount,
        dir_alpha,
        expl_frac,
        visit_softmax_temperature,
    ):
        self.root = None
        self.num_simulations = num_simulations
        self.pb_c_base = pb_c_base
        self.pb_c_init = pb_c_init
        self.discount = discount
        self.dir_alpha = dir_alpha
        self.expl_frac = expl_frac
        self.visit_softmax_temperature = visit_softmax_temperature

    def add_exploration_noise(self):
        noise = np.random.dirichlet([self.dir_alpha] * len(self.root))
        for action, x_a in zip(self.root.actions(), noise):
            self.root[action].add_noise(x_a, self.expl_frac)

    def backpropagate(self, search_path, value):
        for node in reversed(search_path):
            node.add_value(value)
            value = node.reward + self.discount * value

    @staticmethod
    def evaluate_leaf(game, action, network, node):
        game = game.clone()
        reward, observation = game.apply(action)
        if game.terminal:
            value = 0
            legal_actions = []
            policy_logits = []
        else:
            observation = network.preprocess_obs(observation)
            legal_actions = game.legal_actions()
            policy_logits, value = network(observation)
        node.expand(game, reward, legal_actions, policy_logits)
        return value

    @classmethod
    def from_config(cls, config):
        num_simulations = config.num_simulations
        pb_c_base = config.pb_c_base
        pb_c_init = config.pb_c_init
        discount = config.discount
        dir_alpha = config.dir_alpha
        expl_frac = config.expl_frac
        visit_softmax_temperature = config.visit_softmax_temperature
        mcts = cls(num_simulations, pb_c_base, pb_c_init, discount, dir_alpha,
            expl_frac, visit_softmax_temperature)
        return mcts

    def init_play(self, game, network):
        self.root = Node(1)
        reward = 0
        observation = game.make_image()
        legal_actions = game.legal_actions()
        policy_logits, _ = network(observation)
        self.root.expand(game.clone(), reward, legal_actions, policy_logits)

    def play_game(self, game, network):
        game = game.new_game()
        while not game.terminal:
            self.init_play(game, network)
            self.add_exploration_noise()
            self.run(network)
            action = self.select_action(network)
            game.apply(action, record=True)
            game.store_search_statistics(self.root)
            self.root = self.root[action]
        return game

    def run(self, network):
        for _ in range(self.num_simulations):
            node = self.root
            search_path = [node]
            while node.expanded():
                action, node = node.select_child(self.ucb_score)
                search_path.append(node)
            if node.terminal():
                value = 0
            else:
                game = search_path[-2].game
                value = self.evaluate_leaf(game, action, network, node)
            self.backpropagate(search_path, value)

    def select_action(self, network):
        temperature = self.visit_softmax_temperature(network, network)
        action = self.root.select_action(temperature)
        return action

    def ucb_score(self, parent, child):
        pb_c = math.log((parent.visit_count + self.pb_c_base + 1) /
            self.pb_c_base) + self.pb_c_init
        pb_c *= math.sqrt(parent.visit_count) / (child.visit_count + 1)
        prior_score = pb_c * child.prior
        value_score = child.value + prior_score
        return value_score
