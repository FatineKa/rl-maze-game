"""
GameRenderer coordinates window creation and drawing frames using Pygame.
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

COLOR_GOAL = (212, 175, 55)  # Gold highlight color for target cell


class GameRenderer:
    """
    Main Pygame window manager.
    """

    def __init__(self, caption="RL Maze Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        # Center the grid alignment in the window
        dungeon_px_w = GRID_WIDTH * TILE_SIZE
        dungeon_px_h = GRID_HEIGHT * TILE_SIZE
        self.offset_x = (WINDOW_WIDTH - dungeon_px_w) // 2
        self.offset_y = (WINDOW_HEIGHT - dungeon_px_h) // 2

    def draw(self, dungeon, characters, goal=None):
        """
        Draws the game board, target, and characters, then updates display.
        """
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
