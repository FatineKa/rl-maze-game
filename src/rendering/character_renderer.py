"""
Draws characters onto the Pygame screen.

"""

import pygame

from src.game.constants import (
    TILE_SIZE,
    CHARACTER_INSET,
    COLOR_CHARACTER,
)


def draw_character(screen, character, offset_x=0, offset_y=0):
    """
    Draw a character at its current grid position.

    Args:
        screen:    The Pygame surface.
        character: A Character instance.
        offset_x:  Pixel offset of the dungeon's top-left corner.
        offset_y:  Same, vertical.

    The offset args must match what was passed to draw_dungeon, otherwise
    the character will appear in the wrong place relative to the tiles.
    This is exactly the kind of coupling we'll clean up later by introducing
    a Camera class that owns the offset — but for two callers it's fine.
    """
    # Convert grid coordinates to pixel coordinates.
    # The character's tile starts at (offset_x + character.x * TILE_SIZE,
    # offset_y + character.y * TILE_SIZE). We then inset by CHARACTER_INSET
    # so a small border of floor shows around the character.
    pixel_x = offset_x + character.x * TILE_SIZE + CHARACTER_INSET
    pixel_y = offset_y + character.y * TILE_SIZE + CHARACTER_INSET

    # Size after subtracting the inset on both sides.
    size = TILE_SIZE - 2 * CHARACTER_INSET

    rect = pygame.Rect(pixel_x, pixel_y, size, size)
    pygame.draw.rect(screen, COLOR_CHARACTER, rect)