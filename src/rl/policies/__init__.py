"""
Policies: the part of an agent that maps states to actions and learns from them.

Two policies are available:
  - RandomPolicy  : picks actions at random, never learns. Good as a baseline.
  - DynaQPolicy   : Dyna-Q, a tabular RL algorithm. This is the main learner.

BasePolicy defines the interface both share, so the training loop works
identically regardless of which policy is active.
"""

from src.rl.policies.random_policy import RandomPolicy
from src.rl.policies.dyna_q_policy import DynaQPolicy


class BasePolicy:
    """
    Interface shared by every policy.

    select_action picks an action given a state and an exploration rate.
    update folds a transition into the policy's knowledge.
    Policies that don't learn (e.g. random) leave update as a no-op.
    """

    def select_action(self, state, epsilon=0.0):
        raise NotImplementedError

    def update(self, state, action, reward, next_state, next_action, terminated):
        """Learn from one transition. Default: do nothing."""

    def save(self, path):
        """Persist the policy so training can be resumed later."""

    def load(self, path):
        """Restore from a file written by save()."""


def build_policy(name, n_states, n_actions):
    """
    Create a policy by name.

    Args:
        name:      'random' or 'dyna_q'
        n_states:  number of cells in the maze (observation_space.n)
        n_actions: number of directions (action_space.n)

    Returns:
        A policy object.
    """
    name = str(name).lower()
    if name == "random":
        return RandomPolicy(n_actions)
    if name == "dyna_q":
        return DynaQPolicy(n_states, n_actions)
    raise ValueError(f"Unknown policy '{name}'. Choose from: random, dyna_q.")
