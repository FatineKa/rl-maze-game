"""
Movement and collision checks. No state, just functions.
"""

from src.game.constants import TILE_WALL, GRID_WIDTH, GRID_HEIGHT


def is_walkable(dungeon, x, y):
    """
    Returns True if (x, y) is in bounds and not a wall.
    Bounds are checked first — Python's negative indexing would
    silently wrap out-of-range values otherwise.
    """
    if x < 0 or x >= GRID_WIDTH:
        return False
    if y < 0 or y >= GRID_HEIGHT:
        return False

    return dungeon[y][x] != TILE_WALL


def try_move(character, dungeon, dx, dy):
    """
    Moves the character by (dx, dy) if the destination is walkable.
    Returns True if the move happened, False if it was blocked.
    """
    new_x = character.x + dx
    new_y = character.y + dy

    if is_walkable(dungeon, new_x, new_y):
        character.move(dx, dy)
        return True

    return False
