# RL Maze Game

A 2D dungeon where an AI agent learns to navigate from start to goal using
**reinforcement learning** — specifically the **Dyna-Q** algorithm.

Built with Pygame, Gymnasium, and NumPy. No PyTorch required.

<!-- Replace these placeholders with your own captured screenshot and GIF! -->
![AI Agent Gameplay](docs/gameplay.gif)
*Watch the AI agent solve the maze using the Dyna-Q algorithm*

---

## What this project does

The agent starts in the top-left of the maze and has to reach the bottom-right.
It doesn't know the maze layout in advance — it learns by trial and error:

- Every step costs a small penalty → the agent learns to move efficiently.
- Walking into a wall costs extra → the agent learns to avoid walls.
- Reaching the goal gives a big reward → the agent learns where to go.

Over ~1000–2000 episodes the agent goes from wandering randomly to solving the
maze reliably in a small number of steps.

---

## Project layout

```
src/
  config.py          ← all settings in one place (change numbers here)
  game/              ← core game logic (dungeon, movement, collision)
  env/               ← Gymnasium wrapper (turns the game into an RL problem)
  rl/                ← Dyna-Q agent, training loop, evaluation, watch script
  rendering/         ← Pygame drawing
  analysis/          ← metrics logging and training charts
tests/               ← unit tests (pytest)
docs/                ← architecture notes
models/              ← saved Q-table checkpoints (created by training)
results/             ← training metrics CSV and charts (created by training)
```

---

## Setup

Requires **Python 3.11** and a virtual environment (conda or venv).

```bash
# with conda (recommended)
conda activate hermes
pip install -r requirements.txt

# with venv
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Running

### Play the maze yourself (arrow keys / WASD)
```bash
python src/main.py
```

### Train the Dyna-Q agent (headless, fast)
```bash
python -m src.rl.train
python -m src.rl.train --episodes 500 --plot   # shorter run + save charts
```

### Watch the trained agent play
```bash
python -m src.rl.watch                          # trains first, then opens window
python -m src.rl.watch --checkpoint models/dyna_q_final --no-train
```

### Evaluate a saved checkpoint
```bash
python -m src.rl.evaluate models/dyna_q_final
```

### Run the tests
```bash
pytest tests/
```

---

## Training Performance & Charts

When you run training with the `--plot` flag, it automatically generates and updates these three plots in the `results/` folder:

| Training Reward | Success Rate | Steps per Episode |
| :---: | :---: | :---: |
| ![Reward Plot](results/reward.png) | ![Success Rate Plot](results/success_rate.png) | ![Steps Plot](results/steps.png) |

- **Reward**: Shows the total rewards earned per episode. It trends upward as the agent learns.
- **Success Rate**: The percentage of evaluation episodes where the agent reached the goal. It should approach 100% (1.0).
- **Steps**: The number of steps taken to reach the goal. It starts high and decreases to a stable minimum.

---

## Tuning

All settings live in [`src/config.py`](src/config.py). Change a number and re-run — no YAML, no config files.

Key things to try:

| Setting | What it does |
|---|---|
| `PLANNING_STEPS` | More = faster learning, more memory used |
| `ALPHA` | Learning rate. Too high → unstable. Too low → slow. |
| `EPSILON_DECAY` | Lower = explores longer before exploiting |
| `GOAL_REWARD` | Higher = agent is more motivated to reach the goal |

---

## How Dyna-Q works (in brief)

Normal Q-learning updates the agent's knowledge after each real step.
Dyna-Q does the same thing, *plus* replays a handful of past transitions from
memory — as if imagining "what would happen if I did that again?"

Because the maze is deterministic (same move → same result every time),
the model is always correct and planning is very effective. A small number of
planning steps per real step can dramatically speed up learning.

---

## Status

Functional beginner project. The maze is hardcoded; procedural generation is a
natural next step.