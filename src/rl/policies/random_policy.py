"""
Random policy baseline.
"""

import numpy as np


class RandomPolicy:
    """
    Uniformly random action selection for baseline comparison.
    """

    def __init__(self, n_actions, rng=None):
        self.n_actions = n_actions
        self.rng = rng if rng is not None else np.random.default_rng()

    def select_action(self, state, epsilon=0.0):
        return int(self.rng.integers(self.n_actions))

    def update(self, state, action, reward, next_state, next_action, terminated):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass
