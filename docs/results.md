# Results

This file is where training outcomes get recorded as the project matures. The
plotting script writes charts here (`reward.png`, `success_rate.png`,
`steps.png`) from the metrics CSV that training produces.

## How to reproduce

    python -m src.rl.train --episodes 300 --plot
    # writes results/<agent>_metrics.csv and the three PNGs

## What to look for

- **Success rate** climbing toward 1.0 — the agent reaches the goal almost every
  episode once trained.
- **Steps per episode** falling and flattening — it's not just succeeding, it's
  finding a short route.
- **Reward** rising and stabilising — the clearest single summary.

## Baselines

A random policy is the floor to beat: it solves only a small fraction of
episodes on the default 20x15 maze. Any learning agent should clearly exceed it
on success rate and steps-to-goal. Use:

    python -m src.rl.train --agent random --episodes 300

as the reference point when comparing Dyna-Q or DQN runs.

## Smoke-test sanity check

A short Dyna-Q run (~120-150 episodes) on the default layout already reaches a
near-100% success rate, while the random baseline stays well below 20%. If a
change drops Dyna-Q noticeably below that, something regressed.
