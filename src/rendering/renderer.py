"""
Top-level renderer: owns the pygame window and composes the lower-level
dungeon and character drawing into a single frame.

Both the playable game (src/main.py) and the env's human render mode can use
this, so the window setup and centering math live in exactly one place.

pygame is imported at module load here because this module only exists to draw;
anything that wants to stay headless should simply not import it.
"""

import pygame

from src.game.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GRID_WIDTH,
    GRID_HEIGHT,
    TILE_SIZE,
    FPS,
    COLOR_BACKGROUND,
)
from src.rendering.dungeon_renderer import draw_dungeon
from src.rendering.character_renderer import draw_character


# The goal tile isn't part of the base game palette, so give it a colour here.
COLOR_GOAL = (212, 175, 55)  # muted gold


class GameRenderer:
    """Holds the window and draws one frame per draw() call."""

    def __init__(self, caption="RL Maze Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        # Center the grid in the window once; tiles never move.
        dungeon_px_w = GRID_WIDTH * TILE_SIZE
        dungeon_px_h = GRID_HEIGHT * TILE_SIZE
        self.offset_x = (WINDOW_WIDTH - dungeon_px_w) // 2
        self.offset_y = (WINDOW_HEIGHT - dungeon_px_h) // 2

    def draw(self, dungeon, characters, goal=None):
        """
        Render a full frame.

        Args:
            dungeon:    the tile grid.
            characters: an iterable of Character objects to draw.
            goal:       optional (x, y) tile to highlight as the goal.
        """
        # Pump the event queue so the OS keeps the window responsive even when
        # the caller (e.g. an eval loop) isn't handling events itself.
        pygame.event.pump()

        self.screen.fill(COLOR_BACKGROUND)
        draw_dungeon(self.screen, dungeon, self.offset_x, self.offset_y)

        if goal is not None:
            self._draw_goal(goal)

        for character in characters:
            draw_character(self.screen, character, self.offset_x, self.offset_y)

        pygame.display.flip()
        self.clock.tick(FPS)

    def _draw_goal(self, goal):
        gx, gy = goal
        rect = pygame.Rect(
            self.offset_x + gx * TILE_SIZE,
            self.offset_y + gy * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
        pygame.draw.rect(self.screen, COLOR_GOAL, rect)

    def close(self):
        pygame.quit()
