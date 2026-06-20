# Architecture

RL Maze Game is split so that the game can run on its own and the learning code
can reuse the game without dragging in a window. The guiding rule: **game logic
never imports rendering, and rendering never imports pygame into the training
path.**

## Layers

    src/game/        Pure game logic — grid, character, movement. No rendering,
                     no pygame state. Deterministic and trivially testable.
    src/rendering/   All pygame drawing. dungeon_renderer + character_renderer do
                     the primitive drawing; renderer.py (GameRenderer) owns the
                     window and composes a frame.
    src/env/         Gymnasium wrapper. rl_maze_env.py turns the game into a
                     reset()/step() environment; reward.py scores transitions.
    src/rl/          The learner. agent.py drives a policy; policies/ holds the
                     value functions (random, Dyna-Q, DQN); train.py and
                     evaluate.py are the entry points.
    src/analysis/    Metrics logging (CSV) and plotting.
    src/utils/       Config loading, logging setup, asset loading.

## Two entry points

- `src/main.py` — the playable game. Opens a window, reads the keyboard.
- `src/rl/train.py` — headless training. Never opens a window unless asked to
  render.

Both share the same `src/game` code. The environment reuses `create_dungeon`,
`Character`, and the `physics` helpers directly, so the agent plays exactly the
game a human would.

## State and action representation

The observation is a single integer: the agent's cell index, `y * width + x`.
That is what a tabular agent indexes into directly, and a neural agent one-hot
encodes. The goal is fixed for a given layout, so it isn't part of the
observation. Actions are `Discrete(4)`: up, down, left, right.

## Configuration

`config.yaml` is the single source of runtime tuning (reward weights, learning
rates, schedule). Values that must match the hardcoded layout — grid width and
height — live in `src/game/constants.py`, and config mirrors them for the RL
side's convenience. Constants are compile-time truths; config is for things you
tweak between runs.

## Design decisions worth knowing

- **Epsilon lives in the Agent, not the policy.** Every policy shares one decay
  schedule, and the training loop talks to one object.
- **Heavy imports are lazy.** pygame is only imported when something actually
  draws; PyTorch only when the DQN policy is built. Tabular training stays
  light.
- **The model in Dyna-Q is exact** because the maze is deterministic, which is
  why planning is so effective here.
