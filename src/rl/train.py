"""
Training loop: run episodes, let the agent learn, log metrics, checkpoint.

This is the headless entry point for RL training (no game window needed).
All settings are in src/config.py — change the numbers there, then run this.

Usage:
    python -m src.rl.train              # train with Dyna-Q (default)
    python -m src.rl.train --agent random  # baseline: random actions
    python -m src.rl.train --episodes 500 --plot  # short run, then plot
"""

import argparse
import logging
from pathlib import Path

from src.config import (
    EPISODES, EVAL_EVERY, EVAL_EPISODES, SAVE_EVERY,
    CHECKPOINT_DIR, RESULTS_DIR,
)
from src.env.rl_maze_env import RLMazeEnv
from src.rl.agent import Agent
from src.rl.evaluate import evaluate
from src.analysis.logger import MetricsLogger


# Simple console logger — no file writing, no custom config needed.
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("train")


def run_episode(env, agent, training=True):
    """
    Play one full episode.

    Returns (total_reward, steps_taken, solved).

    We choose the *next* action before calling learn() so that on-policy
    algorithms have access to it. Off-policy algorithms (like Dyna-Q) ignore it.
    """
    state, _ = env.reset()
    action = agent.act(state, training=training)
    terminated = truncated = False
    total_reward = 0.0
    steps = 0
    info = {}

    while not (terminated or truncated):
        next_state, reward, terminated, truncated, info = env.step(action)
        next_action = agent.act(next_state, training=training)
        if training:
            agent.learn(state, action, reward, next_state, next_action, terminated)
        state, action = next_state, next_action
        total_reward += reward
        steps += 1

    return total_reward, steps, bool(info.get("is_success"))


def train(agent_name="dyna_q", episodes=None, plot=False):
    """Run the full training schedule."""
    env = RLMazeEnv()
    agent = Agent(env, policy_name=agent_name)
    metrics = MetricsLogger()

    n_episodes = episodes if episodes is not None else EPISODES
    checkpoint_dir = Path(CHECKPOINT_DIR)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    log.info("Training '%s' for %d episodes. Goal is at %s.", agent.name, n_episodes, env.goal)

    for episode in range(1, n_episodes + 1):
        reward, steps, success = run_episode(env, agent, training=True)
        agent.end_episode()
        metrics.log_episode(episode, reward, steps, success, agent.epsilon)

        # Periodic evaluation: run a few greedy episodes (no exploration) to
        # measure how well the policy has learned, separate from noisy training.
        if EVAL_EVERY and episode % EVAL_EVERY == 0:
            stats = evaluate(env, agent, EVAL_EPISODES)
            log.info(
                "ep %4d | ε=%.3f | train reward %+.2f | success %.0f%% | steps %.1f",
                episode,
                agent.epsilon,
                metrics.recent_mean_reward(EVAL_EVERY),
                100 * stats["success_rate"],
                stats["mean_steps"],
            )

        if SAVE_EVERY and episode % SAVE_EVERY == 0:
            path = checkpoint_dir / f"{agent.name}_ep{episode}"
            agent.save(path)
            log.info("Checkpoint saved → %s", path)

    # Save the final model and write the metrics CSV.
    agent.save(checkpoint_dir / f"{agent.name}_final")
    csv_path = metrics.to_csv(f"{RESULTS_DIR}/{agent.name}_metrics.csv")
    log.info("Done. Metrics written to %s", csv_path)

    env.close()
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Train a Dyna-Q agent on the maze.")
    parser.add_argument("--agent", default="dyna_q", choices=["dyna_q", "random"],
                        help="which policy to use (default: dyna_q)")
    parser.add_argument("--episodes", type=int, default=None,
                        help="number of training episodes (overrides config)")
    parser.add_argument("--plot", action="store_true",
                        help="generate training charts when done")
    args = parser.parse_args()

    metrics = train(agent_name=args.agent, episodes=args.episodes)

    if args.plot:
        from src.analysis.plots import plot_training
        csv_name = f"{RESULTS_DIR}/{args.agent}_metrics.csv"
        saved = plot_training(csv_name, RESULTS_DIR)
        for path in saved:
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
