"""
config.py — all tunable settings in one place.

Instead of a YAML file + a custom loader, this project keeps its configuration
as plain Python variables. For a beginner project this is much easier to read:
you can see every setting at a glance, change a number, and run again.

GAME settings control the window and the grid.
RL settings control how the Dyna-Q agent learns.
TRAINING settings control the training loop.
"""

# ---------------------------------------------------------------------------
# Game / display
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Grid size. 20x15 tiles at 32px each = 640x480px dungeon, centred in the window.
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
MAX_STEPS = 500          # episode is cut short after this many steps

# Reward values — tweak these to change how the agent learns.
STEP_PENALTY = -0.01     # small negative reward every step (encourages speed)
WALL_PENALTY = -0.05     # extra penalty for walking into a wall
GOAL_REWARD = 1.0        # big positive reward for reaching the goal

# ---------------------------------------------------------------------------
# Dyna-Q hyperparameters
# ---------------------------------------------------------------------------
GAMMA = 0.99             # discount factor (how much future rewards matter)
EPSILON_START = 1.0      # exploration rate at the start (100% random)
EPSILON_END = 0.05       # minimum exploration rate (5% random)
EPSILON_DECAY = 0.995    # multiplied by epsilon after every episode

ALPHA = 0.1              # learning rate
PLANNING_STEPS = 10      # simulated updates per real step (the "Dyna" part)

# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
EPISODES = 2000          # total training episodes
EVAL_EVERY = 100         # print a progress report every N episodes
EVAL_EPISODES = 20       # episodes to average for the progress report
SAVE_EVERY = 500         # save a checkpoint every N episodes
CHECKPOINT_DIR = "models"
RESULTS_DIR = "results"
