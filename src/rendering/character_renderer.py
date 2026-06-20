"""
Renders a character at their grid position.
"""

import pygame

from src.game.constants import (
    TILE_SIZE,
    CHARACTER_INSET,
    COLOR_CHARACTER,
)


def draw_character(screen, character, offset_x=0, offset_y=0):
    """
    Renders character tile using pixel offsets.
    """
    pixel_x = offset_x + character.x * TILE_SIZE + CHARACTER_INSET
    pixel_y = offset_y + character.y * TILE_SIZE + CHARACTER_INSET
    size = TILE_SIZE - 2 * CHARACTER_INSET

    rect = pygame.Rect(pixel_x, pixel_y, size, size)
    pygame.draw.rect(screen, COLOR_CHARACTER, rect)
