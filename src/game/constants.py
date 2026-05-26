"""
Game-wide constants. Change a value here and it updates everywhere.
"""

# window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# grid
# 20x15 tiles at 32px each = 640x480px of dungeon, centered in the 800x600 window
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15

# tile types stored as ints — faster and lighter than strings
TILE_FLOOR = 0
TILE_WALL = 1

# colors (rgb)
COLOR_BACKGROUND = (116, 145, 97)
COLOR_FLOOR = (102, 59, 23)
COLOR_WALL = (81, 145, 45)
COLOR_FLOOR_OUTLINE = (56, 107, 25)
COLOR_TEXT = (220, 200, 150)

# character is drawn with a small inset so the floor shows around it
CHARACTER_INSET = 4
COLOR_CHARACTER = (200, 110, 90)

# directions as (dx, dy) — y increases downward, so up is -1
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
