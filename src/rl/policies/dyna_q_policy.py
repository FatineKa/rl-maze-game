"""
Dyna-Q: tabular Q-learning with a learned model used for background planning.

How it works (in plain language):
  1. The agent takes a real step and does a normal Q-learning update.
  2. It also remembers that (state, action) → (reward, next_state) in a "model".
  3. After each real step, it replays PLANNING_STEPS random past transitions
     from the model — as if imagining "what if I had done that again?"

Because our maze is deterministic (the same move always leads to the same tile),
the model is always correct. Planning lets reward information propagate across
the maze much faster than learning from real steps alone.

Key variables:
  Q-table   : a 2D array, Q[state][action] = estimated future reward
  alpha     : how fast we update Q (learning rate)
  gamma     : how much we value future rewards vs immediate (discount factor)
  epsilon   : probability of taking a random action (exploration)
"""

import numpy as np

from src.config import ALPHA, GAMMA, PLANNING_STEPS


class DynaQPolicy:
    """Tabular Q-values plus a deterministic environment model."""

    def __init__(self, n_states, n_actions, rng=None):
        self.n_states = n_states
        self.n_actions = n_actions
        self.rng = rng if rng is not None else np.random.default_rng()

        self.alpha = ALPHA
        self.gamma = GAMMA
        self.planning_steps = PLANNING_STEPS

        # Q[state, action] starts at zero.
        # Unvisited actions look as good as visited ones, encouraging exploration.
        self.q = np.zeros((n_states, n_actions), dtype=np.float64)

        # model[(state, action)] = (reward, next_state, terminated)
        # We store every (state, action) pair we've seen so we can replay them.
        self.model = {}
        self._seen = []  # list of (state, action) keys for random sampling

    def select_action(self, state, epsilon=0.0):
        """
        Epsilon-greedy action selection.
        With probability epsilon: pick a random action (explore).
        Otherwise: pick the action with the highest Q-value (exploit).
        """
        if self.rng.random() < epsilon:
            return int(self.rng.integers(self.n_actions))
        return self._greedy_action(state)

    def update(self, state, action, reward, next_state, next_action, terminated):
        """
        Learn from one real transition, then plan from remembered transitions.

        next_action is ignored by Dyna-Q (it's passed in so all policies share
        the same signature, but Q-learning always uses the best possible next
        action rather than the one actually taken).
        """
        # 1. Real Q-learning update from the transition we just observed.
        self._q_update(state, action, reward, next_state, terminated)

        # 2. Store this transition in the model so we can replay it later.
        if (state, action) not in self.model:
            self._seen.append((state, action))
        self.model[(state, action)] = (reward, next_state, terminated)

        # 3. Planning: replay random remembered transitions.
        for _ in range(self.planning_steps):
            idx = self.rng.integers(len(self._seen))
            s, a = self._seen[idx]
            r, s2, term = self.model[(s, a)]
            self._q_update(s, a, r, s2, term)

    def _q_update(self, s, a, r, s2, terminated):
        """One Q-learning update: move Q[s,a] toward the target value."""
        # If the episode ended, there is no next state to bootstrap from.
        best_next = 0.0 if terminated else self.q[s2].max()
        target = r + self.gamma * best_next
        self.q[s, a] += self.alpha * (target - self.q[s, a])

    def _greedy_action(self, state):
        """Return the action with the highest Q-value; break ties randomly."""
        q_s = self.q[state]
        max_q = q_s.max()
        candidates = np.flatnonzero(q_s == max_q)
        return int(self.rng.choice(candidates))

    def save(self, path):
        """Save the Q-table to a .npz file."""
        np.savez(path, q=self.q)

    def load(self, path):
        """Load a previously saved Q-table."""
        candidate = path if str(path).endswith(".npz") else f"{path}.npz"
        with np.load(candidate) as data:
            self.q = data["q"]
