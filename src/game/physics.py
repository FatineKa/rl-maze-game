"""
Movement and collision utility functions.
"""

from src.game.constants import TILE_WALL, GRID_WIDTH, GRID_HEIGHT


def is_walkable(dungeon, x, y):
    """
    Returns True if grid coordinate (x, y) is in bounds and is not a wall.
    """
    if x < 0 or x >= GRID_WIDTH:
        return False
    if y < 0 or y >= GRID_HEIGHT:
        return False

    return dungeon[y][x] != TILE_WALL


def try_move(character, dungeon, dx, dy):
    """
    Updates the character's position if the target cell is walkable.
    Returns True if moved, False if blocked by a wall or boundary.
    """
    new_x = character.x + dx
    new_y = character.y + dy

    if is_walkable(dungeon, new_x, new_y):
        character.move(dx, dy)
        return True

    return False
