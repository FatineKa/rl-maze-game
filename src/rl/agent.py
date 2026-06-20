"""
Agent wrapper coordinates policy action selection and exploration schedules.
"""

import numpy as np

from src.config import EPSILON_START, EPSILON_END, EPSILON_DECAY
from src.rl.policies import build_policy


class Agent:
    """
    Wraps the active learning policy and manages epsilon-greedy exploration.
    """

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
        Select an action. If training, applies epsilon-greedy exploration.
        """
        epsilon = self.epsilon if training else 0.0
        return self.policy.select_action(state, epsilon)

    def learn(self, state, action, reward, next_state, next_action, terminated):
        """
        Pass transition details to update the underlying policy.
        """
        self.policy.update(state, action, reward, next_state, next_action, terminated)

    def end_episode(self):
        """
        Decay exploration rate after each episode down to the minimum floor.
        """
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def save(self, path):
        self.policy.save(path)

    def load(self, path):
        self.policy.load(path)
