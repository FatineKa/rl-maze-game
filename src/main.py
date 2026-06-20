"""
Playable manual-controlled entry point for the game.
"""

import sys
import pygame

from src.game.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    GRID_WIDTH,
    GRID_HEIGHT,
    TILE_SIZE,
    COLOR_BACKGROUND,
    DIRECTION_UP,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
)
from src.game.dungeon import create_dungeon
from src.game.character import Character
from src.game.physics import try_move, is_walkable
from src.rendering.dungeon_renderer import draw_dungeon
from src.rendering.character_renderer import draw_character

KEY_TO_DIRECTION = {
    pygame.K_UP: DIRECTION_UP,
    pygame.K_DOWN: DIRECTION_DOWN,
    pygame.K_LEFT: DIRECTION_LEFT,
    pygame.K_RIGHT: DIRECTION_RIGHT,
    pygame.K_w: DIRECTION_UP,
    pygame.K_s: DIRECTION_DOWN,
    pygame.K_a: DIRECTION_LEFT,
    pygame.K_d: DIRECTION_RIGHT,
}


def find_spawn_point(dungeon):
    """
    Finds the first walkable tile scanning from top-left.
    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if is_walkable(dungeon, x, y):
                return x, y

    raise RuntimeError("Dungeon has no walkable tiles for spawn.")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("RL Maze Game")
    clock = pygame.time.Clock()

    dungeon = create_dungeon()
    spawn_x, spawn_y = find_spawn_point(dungeon)
    player = Character(spawn_x, spawn_y)

    # Offset to center grid inside the screen window
    dungeon_pixel_width = GRID_WIDTH * TILE_SIZE
    dungeon_pixel_height = GRID_HEIGHT * TILE_SIZE
    offset_x = (WINDOW_WIDTH - dungeon_pixel_width) // 2
    offset_y = (WINDOW_HEIGHT - dungeon_pixel_height) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue

                direction = KEY_TO_DIRECTION.get(event.key)
                if direction is not None:
                    dx, dy = direction
                    try_move(player, dungeon, dx, dy)

        screen.fill(COLOR_BACKGROUND)
        draw_dungeon(screen, dungeon, offset_x, offset_y)
        draw_character(screen, player, offset_x, offset_y)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
