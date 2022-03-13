from torch.optim import AdamW


class AlphaZeroConfig:
    def __init__(
        self,
        num_simulations=400,
        dir_alpha=0.3,
        expl_frac=0.25,
        pb_c_base=19652,
        pb_c_init = 1.25,
        visit_softmax_temperature=lambda *_: 0.5,
        device=None,
        training_device=None,
        window_size=400,
        batch_size=256,
        td_steps=None,
        n_batchs_per_game=15,
        n_self_play_games=1000,
        optimizer=AdamW,
        learning_rate=0.001,
        weight_decay=0.01,
        optimizer_specific_args={},
    ):
        self.num_simulations = num_simulations
        self.dir_alpha = dir_alpha
        self.expl_frac = expl_frac
        self.pb_c_base = pb_c_base
        self.pb_c_init = pb_c_init
        self.visit_softmax_temperature = visit_softmax_temperature
        self.device = device
        self.training_device = training_device
        self.window_size = window_size
        self.batch_size = batch_size
        self.td_steps = td_steps
        self.n_batchs_per_game = n_batchs_per_game
        self.n_self_play_games = n_self_play_games
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.optimizer_specific_args = optimizer_specific_args
        self.weight_decay = weight_decay

    @property
    def optimizer_args(self):
        optimizer_args = {'lr': self.learning_rate, 'weight_decay': self.weight_decay}
        optimizer_args.update(self.optimizer_specific_args)
        return optimizer_args
