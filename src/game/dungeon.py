"""
Builds the dungeon grid.
Currently hardcoded — will be replaced with procedural generation.
"""

from src.game.constants import (
    GRID_WIDTH,
    GRID_HEIGHT,
    TILE_FLOOR,
    TILE_WALL,
)


# '#' = wall, '.' = floor
# written as strings so the layout is readable in source
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
    Converts the raw layout into a 2D list of tile ints.
    grid[y][x] gives the tile at column x, row y.
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

    # catch mismatches between the layout and the declared grid size
    assert len(grid) == GRID_HEIGHT, (
        f"Layout has {len(grid)} rows but GRID_HEIGHT is {GRID_HEIGHT}"
    )
    assert all(len(row) == GRID_WIDTH for row in grid), (
        f"Layout rows must all be {GRID_WIDTH} columns wide"
    )

    return grid
