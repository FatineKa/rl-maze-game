"""
Renders a trained agent navigating the maze in a Pygame window.
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
    Loads or trains an agent, then renders greedy episodes.
    """
    setup_env = RLMazeEnv()
    agent = Agent(setup_env, policy_name=agent_name)

    if checkpoint:
        agent.load(checkpoint)
        log.info("Loaded checkpoint: %s", checkpoint)
    else:
        log.info("Training '%s' for %d episodes before rendering...", agent.name, train_episodes)
        for _ in range(train_episodes):
            run_episode(setup_env, agent, training=True)
            agent.end_episode()
        log.info("Training complete. Opening window.")
    setup_env.close()

    import pygame

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
                action = agent.act(state, training=False)
                state, _, terminated, truncated, info = env.step(action)
                env.render()
                steps += 1
                time.sleep(step_delay)

            outcome = "reached goal ✓" if info.get("is_success") else "failed ✗"
            log.info("Rollout %d: %s in %d steps", episode, outcome, steps)
            time.sleep(0.8)
    finally:
        env.close()


def _should_quit(pygame):
    """Returns True if the user closes the window or presses Escape."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Watch a trained agent solve the maze.")
    parser.add_argument("--agent", default="dyna_q", choices=["dyna_q", "random"],
                        help="Policy to use (default: dyna_q)")
    parser.add_argument("--checkpoint", default=None,
                        help="Path to checkpoint file")
    parser.add_argument("--no-train", action="store_true",
                        help="Skip training phase (requires --checkpoint)")
    parser.add_argument("--episodes", type=int, default=1000,
                        help="Training episodes if training is run (default: 1000)")
    parser.add_argument("--fps", type=int, default=8,
                        help="Steps rendered per second (default: 8)")
    parser.add_argument("--rollouts", type=int, default=3,
                        help="Number of episodes to watch (default: 3)")
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
