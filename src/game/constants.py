"""
Game-wide constants and color definitions.
"""

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT  # noqa: F401

# Tile definitions
TILE_FLOOR = 0
TILE_WALL = 1

# Colors (RGB)
COLOR_BACKGROUND = (116, 145, 97)
COLOR_FLOOR = (102, 59, 23)
COLOR_WALL = (81, 145, 45)
COLOR_FLOOR_OUTLINE = (56, 107, 25)
COLOR_TEXT = (220, 200, 150)

# Rendering settings
CHARACTER_INSET = 4
COLOR_CHARACTER = (200, 110, 90)

# Movement vectors
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
