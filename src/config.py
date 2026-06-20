"""
Configuration and hyperparameter settings.
"""

# ---------------------------------------------------------------------------
# Game & Display settings
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Grid dimensions (20x15 tiles of 32px each)
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15

# ---------------------------------------------------------------------------
# Environment settings
# ---------------------------------------------------------------------------
MAX_STEPS = 500          # Maximum steps per episode

# Reward structure
STEP_PENALTY = -0.01     # Penalty per step to encourage speed
WALL_PENALTY = -0.05     # Penalty for collision with walls
GOAL_REWARD = 1.0        # Reward for reaching the target

# ---------------------------------------------------------------------------
# Dyna-Q Hyperparameters
# ---------------------------------------------------------------------------
GAMMA = 0.99             # Discount factor
EPSILON_START = 1.0      # Initial exploration rate
EPSILON_END = 0.05       # Minimum exploration rate
EPSILON_DECAY = 0.995    # Decay multiplier per episode

ALPHA = 0.1              # Learning rate
PLANNING_STEPS = 10      # Simulated planning steps per real step

# ---------------------------------------------------------------------------
# Training configurations
# ---------------------------------------------------------------------------
EPISODES = 2000          # Total training runs
EVAL_EVERY = 100         # Interval for progress reporting
EVAL_EPISODES = 20       # Number of evaluation episodes
SAVE_EVERY = 500         # Checkpoint interval
CHECKPOINT_DIR = "models"
RESULTS_DIR = "results"
