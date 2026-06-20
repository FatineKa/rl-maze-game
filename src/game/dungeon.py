"""
Generates the dungeon grid from a hardcoded layout template.
"""

from src.game.constants import (
    GRID_WIDTH,
    GRID_HEIGHT,
    TILE_FLOOR,
    TILE_WALL,
)

# Template representation of the maze: '#' is wall, '.' is floor
_RAW_LAYOUT = [
    "####################",
    "#..................#",
    "#..................#",
    "#..####............#",
    "#.....#............#",
    "#.....#......####..#",
    "#.....#......#..#..#",
    "#.....#......#..#..#",
    "#............#..#..#",
    "#............####..#",
    "#..................#",
    "#......####........#",
    "#......#..#........#",
    "#......####........#",
    "####################",
]


def create_dungeon():
    """
    Parses _RAW_LAYOUT into a 2D list of tile integers.
    grid[y][x] returns the tile at column x, row y.
    """
    grid = []

    for y, row in enumerate(_RAW_LAYOUT):
        row_tiles = []
        for x, char in enumerate(row):
            if char == "#":
                row_tiles.append(TILE_WALL)
            else:
                row_tiles.append(TILE_FLOOR)
        grid.append(row_tiles)

    # Validate template matches configuration dimensions
    assert len(grid) == GRID_HEIGHT, (
        f"Layout has {len(grid)} rows but GRID_HEIGHT is {GRID_HEIGHT}"
    )
    assert all(len(row) == GRID_WIDTH for row in grid), (
        f"Layout rows must all be {GRID_WIDTH} columns wide"
    )

    return grid
