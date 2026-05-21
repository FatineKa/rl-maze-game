"""
Movement and collision rules.

This module answers questions like "can this character move to (x, y)?"
without itself doing any moving. It's a pure-logic module: no Pygame,
no state, just functions that take inputs and return answers.

"""

from src.game.constants import TILE_WALL, GRID_WIDTH, GRID_HEIGHT


def is_walkable(dungeon, x, y):
    """
    Return True if (x, y) is a valid tile to stand on.

    A tile is walkable when:
      - It's inside the grid bounds.
      - It's not a wall.

    Order matters: we check bounds first. Otherwise indexing into
    dungeon[y][x] with out-of-range values would crash.
    """
    # Bounds check. Negative indices in Python silently wrap to the end
    # of a list, which would let the character teleport .
    if x < 0 or x >= GRID_WIDTH:
        return False
    if y < 0 or y >= GRID_HEIGHT:
        return False

    # Now safe to index. Look up the tile type at this position.
    tile = dungeon[y][x]

    # Currently only walls block movement. Later we might add doors
    # (walkable if open), pits, etc. — easy to extend by adding cases here.
    return tile != TILE_WALL


def try_move(character, dungeon, dx, dy):
    """
    Attempt to move the character by (dx, dy). Apply the move only
    if the destination is walkable.

    Returns True if the move happened, False if blocked.

    Why return a bool? Because the caller often wants to react —
    play a "bump" sound if blocked, count steps if moved, etc. Even
    if we don't use the return value yet, it costs nothing to expose
    it and saves a refactor later.
    """
    new_x = character.x + dx
    new_y = character.y + dy

    if is_walkable(dungeon, new_x, new_y):
        character.move(dx, dy)
        return True

    return False