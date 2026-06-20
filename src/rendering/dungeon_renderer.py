"""
Renders the dungeon tiles grid.
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
    Iterates and renders the dungeon tiles.
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
                pygame.draw.rect(screen, COLOR_FLOOR_OUTLINE, rect, 1)
