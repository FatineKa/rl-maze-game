"""
Policy definitions mapping states to actions.
"""

from src.rl.policies.random_policy import RandomPolicy
from src.rl.policies.dyna_q_policy import DynaQPolicy


class BasePolicy:
    """
    Common interface for all policies.
    """

    def select_action(self, state, epsilon=0.0):
        raise NotImplementedError

    def update(self, state, action, reward, next_state, next_action, terminated):
        """Learn from transition. Default implementation is a no-op."""

    def save(self, path):
        """Save the policy parameters to disk."""

    def load(self, path):
        """Load policy parameters from disk."""


def build_policy(name, n_states, n_actions):
    """
    Instantiates a policy by name.
    """
    name = str(name).lower()
    if name == "random":
        return RandomPolicy(n_actions)
    if name == "dyna_q":
        return DynaQPolicy(n_states, n_actions)
    raise ValueError(f"Unknown policy '{name}'. Options: random, dyna_q.")
