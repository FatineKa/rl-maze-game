"""
Watch a trained agent solve the maze in the game window.

This is the "see the AI play" entry point. src/main.py is human-controlled;
this script lets a trained policy drive, so you can watch the agent navigate
from spawn to goal.

By default it trains a fresh Dyna-Q agent quickly (no window), then opens the
window and runs a few greedy episodes at a speed you can actually watch.
You can also load a saved checkpoint to skip training entirely.

Usage:
    python -m src.rl.watch                              # train, then watch
    python -m src.rl.watch --episodes 500               # train less
    python -m src.rl.watch --checkpoint models/dyna_q_final --no-train
    python -m src.rl.watch --fps 6 --rollouts 5
"""

import argparse
import logging
import time

from src.env.rl_maze_env import RLMazeEnv
from src.rl.agent import Agent
from src.rl.train import run_episode


logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("watch")


def watch(agent_name="dyna_q", train_episodes=1000, checkpoint=None, fps=8, rollouts=3):
    """
    Build an agent (trained headlessly or loaded from disk), then render rollouts.

    Args:
        agent_name:     'dyna_q' or 'random'
        train_episodes: episodes to train if no checkpoint is given
        checkpoint:     path to a saved policy; skips training when provided
        fps:            agent moves per second in the window
        rollouts:       number of full episodes to watch
    """
    # Train (or load) using a headless env so setup is fast.
    setup_env = RLMazeEnv()
    agent = Agent(setup_env, policy_name=agent_name)

    if checkpoint:
        agent.load(checkpoint)
        log.info("Loaded checkpoint: %s", checkpoint)
    else:
        log.info("Training '%s' for %d episodes before watching...", agent.name, train_episodes)
        for _ in range(train_episodes):
            run_episode(setup_env, agent, training=True)
            agent.end_episode()
        log.info("Training done. Opening window...")
    setup_env.close()

    # Open the window and let the greedy agent play.
    import pygame  # local import — only needed for the visible part

    env = RLMazeEnv(render_mode="human")
    step_delay = 1.0 / max(fps, 1)

    try:
        for episode in range(1, rollouts + 1):
            state, _ = env.reset()
            env.render()
            terminated = truncated = False
            steps = 0

            while not (terminated or truncated):
                if _should_quit(pygame):
                    log.info("Window closed.")
                    return
                action = agent.act(state, training=False)  # greedy, no exploration
                state, _, terminated, truncated, info = env.step(action)
                env.render()
                steps += 1
                time.sleep(step_delay)

            outcome = "reached goal ✓" if info.get("is_success") else "gave up ✗"
            log.info("Rollout %d: %s in %d steps", episode, outcome, steps)
            time.sleep(0.8)  # brief pause between episodes
    finally:
        env.close()


def _should_quit(pygame):
    """Returns True if the user closed the window or pressed Escape."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Watch a trained agent solve the maze.")
    parser.add_argument("--agent", default="dyna_q", choices=["dyna_q", "random"],
                        help="which agent to train/watch (default: dyna_q)")
    parser.add_argument("--checkpoint", default=None,
                        help="path to a saved policy (e.g. models/dyna_q_final)")
    parser.add_argument("--no-train", action="store_true",
                        help="skip training (use together with --checkpoint)")
    parser.add_argument("--episodes", type=int, default=1000,
                        help="training episodes before watching (default: 1000)")
    parser.add_argument("--fps", type=int, default=8,
                        help="agent moves shown per second (default: 8)")
    parser.add_argument("--rollouts", type=int, default=3,
                        help="number of episodes to watch (default: 3)")
    args = parser.parse_args()

    train_ep = 0 if args.no_train else args.episodes
    watch(
        agent_name=args.agent,
        train_episodes=train_ep,
        checkpoint=args.checkpoint,
        fps=args.fps,
        rollouts=args.rollouts,
    )


if __name__ == "__main__":
    main()
