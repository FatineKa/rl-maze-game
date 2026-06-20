"""
Tests for the Gymnasium maze environment.

Runnable with pytest (`pytest tests/`) or directly (`python tests/test_env.py`).
"""

import os
import sys

# Make the project root importable when run directly.
# (pytest handles this automatically; this covers running the file by path.)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.env.rl_maze_env import RLMazeEnv
from src.game.character import Character
from src.config import STEP_PENALTY, WALL_PENALTY, GOAL_REWARD


def _make_env(max_steps=None):
    env = RLMazeEnv(render_mode="ansi")
    if max_steps is not None:
        env.max_steps = max_steps
    return env


def test_spaces():
    env = _make_env()
    assert env.action_space.n == 4
    assert env.observation_space.n == env.width * env.height


def test_reset_returns_valid_observation():
    env = _make_env()
    obs, info = env.reset(seed=0)
    assert env.observation_space.contains(obs)
    for key in ("agent", "goal", "is_success"):
        assert key in info
    assert info["agent"] == env.spawn


def test_encode_decode_roundtrip():
    env = _make_env()
    for (x, y) in [(0, 0), (1, 1), (env.width - 1, env.height - 1), env.goal]:
        assert env.decode(env._encode(x, y)) == (x, y)


def test_walking_into_wall_is_blocked_and_penalised():
    env = _make_env()
    env.reset(seed=0)  # spawn at (1, 1)
    before = (env.agent.x, env.agent.y)
    # Action 0 is "up", which from (1, 1) walks into the top border wall.
    obs, reward, terminated, truncated, info = env.step(0)
    assert info["hit_wall"] is True
    assert (env.agent.x, env.agent.y) == before  # didn't move
    assert reward == STEP_PENALTY + WALL_PENALTY   # both penalties applied
    assert not terminated


def test_reaching_goal_terminates_with_reward():
    env = _make_env()
    env.reset()
    gx, gy = env.goal
    # Place the agent one tile above the goal and step down onto it.
    env.agent = Character(gx, gy - 1)
    obs, reward, terminated, truncated, info = env.step(1)  # 1 = down
    assert terminated is True
    assert info["is_success"] is True
    assert reward == GOAL_REWARD


def test_truncation_at_step_limit():
    env = _make_env(max_steps=5)
    env.reset(seed=0)
    truncated = False
    for _ in range(5):
        _, _, terminated, truncated, _ = env.step(0)  # bump the wall repeatedly
    assert truncated is True


def test_layout_is_deterministic():
    a = _make_env()
    b = _make_env()
    assert a.spawn == b.spawn
    assert a.goal == b.goal


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all env tests passed")
