"""
Evaluation: measure how good a policy is right now.

evaluate() runs several greedy episodes (no exploration, no learning) and
reports the averages: reward, success rate, and steps to reach the goal.

It is called periodically during training and can also be run standalone
against a saved checkpoint:

    python -m src.rl.evaluate models/dyna_q_final
"""

import argparse
import logging

from src.config import EVAL_EPISODES
from src.env.rl_maze_env import RLMazeEnv
from src.rl.agent import Agent


logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("eval")


def evaluate(env, agent, episodes):
    """
    Run `episodes` greedy episodes and return aggregate metrics.

    Returns a dict: mean_reward, success_rate, mean_steps.
    mean_steps is averaged over successful episodes only (a failed episode
    just hits the step limit, which would skew the average).
    """
    total_reward = 0.0
    successes = 0
    steps_on_success = []

    for _ in range(episodes):
        state, _ = env.reset()
        terminated = truncated = False
        ep_reward = 0.0
        ep_steps = 0

        while not (terminated or truncated):
            action = agent.act(state, training=False)
            state, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            ep_steps += 1

        total_reward += ep_reward
        if info.get("is_success"):
            successes += 1
            steps_on_success.append(ep_steps)

    mean_steps = (
        sum(steps_on_success) / len(steps_on_success) if steps_on_success else float("nan")
    )
    return {
        "mean_reward": total_reward / episodes,
        "success_rate": successes / episodes,
        "mean_steps": mean_steps,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate a saved policy checkpoint.")
    parser.add_argument("checkpoint", help="path to a checkpoint (e.g. models/dyna_q_final)")
    parser.add_argument("--agent", default="dyna_q", choices=["dyna_q", "random"],
                        help="which policy type was saved (default: dyna_q)")
    parser.add_argument("--episodes", type=int, default=EVAL_EPISODES,
                        help="number of evaluation episodes")
    args = parser.parse_args()

    env = RLMazeEnv()
    agent = Agent(env, policy_name=args.agent)
    agent.load(args.checkpoint)

    metrics = evaluate(env, agent, args.episodes)
    env.close()

    log.info(
        "Eval over %d episodes | reward %.3f | success %.0f%% | steps %.1f",
        args.episodes,
        metrics["mean_reward"],
        100 * metrics["success_rate"],
        metrics["mean_steps"],
    )


if __name__ == "__main__":
    main()
