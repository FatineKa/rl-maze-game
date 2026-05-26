"""
Draws the dungeon grid to the screen.
"""

import pygame

from src.game.constants import (
    TILE_SIZE,
    TILE_FLOOR,
    TILE_WALL,
    COLOR_FLOOR,
    COLOR_WALL,
    COLOR_FLOOR_OUTLINE,
)


def draw_dungeon(screen, dungeon, offset_x=0, offset_y=0):
    """
    Draws every tile of the dungeon.
    offset_x/offset_y shift the whole grid to center it in the window.
    """
    for y, row in enumerate(dungeon):
        for x, tile in enumerate(row):
            pixel_x = offset_x + x * TILE_SIZE
            pixel_y = offset_y + y * TILE_SIZE
            rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)

            if tile == TILE_WALL:
                pygame.draw.rect(screen, COLOR_WALL, rect)
            elif tile == TILE_FLOOR:
                pygame.draw.rect(screen, COLOR_FLOOR, rect)
                # thin outline to make the grid visible
                pygame.draw.rect(screen, COLOR_FLOOR_OUTLINE, rect, 1)
