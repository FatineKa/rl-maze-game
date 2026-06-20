"""
Dyna-Q policy implementation combining Q-learning with a model for planning.
"""

import numpy as np

from src.config import ALPHA, GAMMA, PLANNING_STEPS


class DynaQPolicy:
    """
    Tabular Q-learning with simulated experience replay from a deterministic model.
    """

    def __init__(self, n_states, n_actions, rng=None):
        self.n_states = n_states
        self.n_actions = n_actions
        self.rng = rng if rng is not None else np.random.default_rng()

        self.alpha = ALPHA
        self.gamma = GAMMA
        self.planning_steps = PLANNING_STEPS

        # Initialize Q-values to zero
        self.q = np.zeros((n_states, n_actions), dtype=np.float64)

        # Transition model map: (state, action) -> (reward, next_state, terminated)
        self.model = {}
        self._seen = []

    def select_action(self, state, epsilon=0.0):
        """
        Epsilon-greedy action selection.
        """
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.n_actions))
        return self._greedy_action(state)

    def update(self, state, action, reward, next_state, next_action, terminated):
        """
        Performs a Q-value update on the real transition, records it in the model,
        and runs planning updates on random transitions from the model.
        """
        # Update Q-table with real transition
        self._q_update(state, action, reward, next_state, terminated)

        # Record transition in model
        if (state, action) not in self.model:
            self._seen.append((state, action))
        self.model[(state, action)] = (reward, next_state, terminated)

        # Planning phase: replay random transitions from the model
        for _ in range(self.planning_steps):
            idx = self.rng.integers(len(self._seen))
            s, a = self._seen[idx]
            r, s2, term = self.model[(s, a)]
            self._q_update(s, a, r, s2, term)

    def _q_update(self, s, a, r, s2, terminated):
        """
        Single Q-value update step.
        """
        best_next = 0.0 if terminated else self.q[s2].max()
        target = r + self.gamma * best_next
        self.q[s, a] += self.alpha * (target - self.q[s, a])

    def _greedy_action(self, state):
        """
        Returns the action with the maximum Q-value, breaking ties randomly.
        """
        q_s = self.q[state]
        max_q = q_s.max()
        candidates = np.flatnonzero(q_s == max_q)
        return int(self.rng.choice(candidates))

    def save(self, path):
        np.savez(path, q=self.q)

    def load(self, path):
        candidate = path if str(path).endswith(".npz") else f"{path}.npz"
        loaded = np.load(candidate)
        self.q = loaded["q"]
