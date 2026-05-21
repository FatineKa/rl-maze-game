"""
Game-wide constants.

These values are referenced across many modules. Keeping them in one place
means we change them once instead of hunting through code. 
"""

# Window
# The size of the Pygame window in pixels. Standard 4:3 ratio, comfortable
# We may make this configurable later via config.yaml.
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60  # Target frames per second for the game loop


# Grid
# The dungeon is a grid of cells. Each cell is one "tile" the character
# can stand on (if walkable) or bump into (if wall).
#
# TILE_SIZE is how many pixels wide each tile is when drawn. 
TILE_SIZE = 32

# How many tiles fit in the dungeon. We make the dungeon smaller than the
# window so we have margin around it for UI later (HUD, minimap, etc.).
# 20 wide x 15 tall = 640x480 pixels of dungeon, leaving 160 horizontal
# and 120 vertical pixels of slack inside our 800x600 window.
GRID_WIDTH = 20
GRID_HEIGHT = 15


# Tile types

# Each cell in the dungeon stores an integer representing what kind of tile
# it is. Using integers (not strings) is faster and uses less memory 
#
# We give them meaningful names for better readability

TILE_FLOOR = 0  # Walkable ground
TILE_WALL = 1   # Solid wall, blocks movement


# Colors
# Pygame colors are (Red, Green, Blue) tuples, each 0-255.

COLOR_BACKGROUND = (116, 145, 97)      
COLOR_FLOOR = (102, 59, 23)           
COLOR_WALL = (81, 145,45)           
COLOR_FLOOR_OUTLINE = (56, 107, 25)   
COLOR_TEXT = (220, 200, 150)         


# Character
# The player character will be drawn as a square filling most (but not all)
# of its tile, with a small inset so we can see the floor around it.
# This makes the character visually distinct from the tiles themselves.
CHARACTER_INSET = 4  # Pixels of margin inside the tile

# A warm, slightly desaturated red — readable on the muted dungeon palette
# without screaming for attention. We'll customize this per-user later.
COLOR_CHARACTER = (200, 110, 90)


# Movement
# Directions as (dx, dy) tuples. dx is column change, dy is row change.
# y increases downward in screen coordinates — that's why UP is -1.
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)