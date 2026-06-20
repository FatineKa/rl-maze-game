"""
Tests for the dungeon layout and walkability checks.

Runnable with pytest (`pytest tests/`) or directly (`python tests/test_dungeon.py`).
"""

import os
import sys

# Make the project root importable when this file is run directly
# (pytest handles this automatically; this covers running the file by path).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game.constants import GRID_WIDTH, GRID_HEIGHT, TILE_FLOOR, TILE_WALL
from src.game.dungeon import create_dungeon
from src.game.physics import is_walkable


def test_dimensions_match_constants():
    grid = create_dungeon()
    assert len(grid) == GRID_HEIGHT
    assert all(len(row) == GRID_WIDTH for row in grid)


def test_only_known_tile_types():
    grid = create_dungeon()
    tiles = {tile for row in grid for tile in row}
    assert tiles <= {TILE_FLOOR, TILE_WALL}


def test_border_is_walled():
    grid = create_dungeon()
    # Top and bottom rows.
    assert all(tile == TILE_WALL for tile in grid[0])
    assert all(tile == TILE_WALL for tile in grid[-1])
    # Left and right columns.
    assert all(row[0] == TILE_WALL for row in grid)
    assert all(row[-1] == TILE_WALL for row in grid)


def test_has_open_floor():
    grid = create_dungeon()
    floor_count = sum(tile == TILE_FLOOR for row in grid for tile in row)
    assert floor_count > 0


def test_is_walkable_bounds_and_walls():
    grid = create_dungeon()
    # Out of bounds in every direction.
    assert not is_walkable(grid, -1, 0)
    assert not is_walkable(grid, 0, -1)
    assert not is_walkable(grid, GRID_WIDTH, 0)
    assert not is_walkable(grid, 0, GRID_HEIGHT)
    # Corner is a wall; an interior floor tile is walkable.
    assert not is_walkable(grid, 0, 0)
    assert is_walkable(grid, 1, 1)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all dungeon tests passed")
