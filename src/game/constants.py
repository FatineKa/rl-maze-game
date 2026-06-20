"""
Game-wide constants. Change a value here and it updates everywhere.

Grid size and window dimensions come from src/config.py so there is a single
source of truth for all tunable settings.
"""

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT  # noqa: F401

# Tile types stored as ints — faster and lighter than strings.
TILE_FLOOR = 0
TILE_WALL = 1

# Colors (RGB)
COLOR_BACKGROUND = (116, 145, 97)
COLOR_FLOOR = (102, 59, 23)
COLOR_WALL = (81, 145, 45)
COLOR_FLOOR_OUTLINE = (56, 107, 25)
COLOR_TEXT = (220, 200, 150)

# The character is drawn with a small inset so the floor shows around it.
CHARACTER_INSET = 4
COLOR_CHARACTER = (200, 110, 90)

# Directions as (dx, dy) — y increases downward, so up is -1.
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
