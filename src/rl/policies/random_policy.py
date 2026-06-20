"""
A policy that ignores the state and picks uniformly at random.

Useful as a baseline (how well does pure chance do?) and as the simplest
possible check that the env/agent/training plumbing all fit together.
"""

import numpy as np


class RandomPolicy:
    """Uniform random action selection; learns nothing."""

    def __init__(self, n_actions, rng=None):
        self.n_actions = n_actions
        self.rng = rng if rng is not None else np.random.default_rng()

    def select_action(self, state, epsilon=0.0):
        # epsilon is irrelevant here, but kept in the signature so this policy
        # is a drop-in for the others.
        return int(self.rng.integers(self.n_actions))

    def update(self, state, action, reward, next_state, next_action, terminated):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass
