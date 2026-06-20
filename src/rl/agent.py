"""
The learning agent: a policy + an exploration schedule.

The Agent is the object the training loop talks to. It wraps whichever policy
is active (random or dyna_q) and manages the epsilon schedule:

  - At the start of training, epsilon = 1.0 → the agent acts completely randomly.
  - After every episode, epsilon decays: epsilon = epsilon * EPSILON_DECAY.
  - Epsilon never drops below EPSILON_END, so the agent keeps exploring a little.

Why do we need exploration? Because the agent needs to visit parts of the maze
it hasn't seen yet — it can't learn from experience it never had.
"""

import numpy as np

from src.config import EPSILON_START, EPSILON_END, EPSILON_DECAY
from src.rl.policies import build_policy


class Agent:
    """Wraps a policy and manages epsilon-greedy exploration."""

    def __init__(self, env, policy_name="dyna_q"):
        n_states = env.observation_space.n
        n_actions = env.action_space.n

        self.rng = np.random.default_rng()
        self.policy = build_policy(policy_name, n_states, n_actions)
        self.name = policy_name

        self.epsilon = EPSILON_START
        self.epsilon_end = EPSILON_END
        self.epsilon_decay = EPSILON_DECAY

    def act(self, state, training=True):
        """
        Choose an action.
        During training: use epsilon-greedy (random sometimes).
        During evaluation: act greedily (always pick the best known action).
        """
        epsilon = self.epsilon if training else 0.0
        return self.policy.select_action(state, epsilon)

    def learn(self, state, action, reward, next_state, next_action, terminated):
        """Pass a transition to the policy so it can update its Q-values."""
        self.policy.update(state, action, reward, next_state, next_action, terminated)

    def end_episode(self):
        """Decay exploration after each episode, but never below the floor."""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def save(self, path):
        self.policy.save(path)

    def load(self, path):
        self.policy.load(path)
