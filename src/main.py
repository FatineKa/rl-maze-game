"""
Hermes — entry point.

Opens the Pygame window and runs the main game loop. The player can
move a character through a hardcoded dungeon using the arrow keys.
Movement is discrete: one key-press equals one tile.
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


# Mapping from Pygame key codes to direction vectors.
# Defining this as a module-level dict means the event loop below
# stays clean — no long if/elif chain for every arrow key.
KEY_TO_DIRECTION = {
    pygame.K_UP: DIRECTION_UP,
    pygame.K_DOWN: DIRECTION_DOWN,
    pygame.K_LEFT: DIRECTION_LEFT,
    pygame.K_RIGHT: DIRECTION_RIGHT,
    # WASD as alternatives, because some people prefer them.
    pygame.K_w: DIRECTION_UP,
    pygame.K_s: DIRECTION_DOWN,
    pygame.K_a: DIRECTION_LEFT,
    pygame.K_d: DIRECTION_RIGHT,
}


def find_spawn_point(dungeon):
    """
    Find the first walkable tile in the dungeon to spawn the character.

    We scan left-to-right, top-to-bottom, so this finds the upper-left-most
    floor tile. Good enough for a hardcoded dungeon; later we'll have the
    procedural generator designate a proper spawn point.
    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if is_walkable(dungeon, x, y):
                return x, y

    # If no walkable tile exists, the dungeon is malformed.
    # Better to fail loudly than spawn the player inside a wall.
    raise RuntimeError("Dungeon has no walkable tiles for spawn.")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hermes")
    clock = pygame.time.Clock()

    # Build the world.
    dungeon = create_dungeon()
    spawn_x, spawn_y = find_spawn_point(dungeon)
    player = Character(spawn_x, spawn_y)

    # Center the dungeon in the window (same math as before).
    dungeon_pixel_width = GRID_WIDTH * TILE_SIZE
    dungeon_pixel_height = GRID_HEIGHT * TILE_SIZE
    offset_x = (WINDOW_WIDTH - dungeon_pixel_width) // 2
    offset_y = (WINDOW_HEIGHT - dungeon_pixel_height) // 2

    running = True
    while running:

        # --- 1. Handle events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue

                # Did this key map to a movement direction?
                # .get() returns None if the key isn't in our mapping —
                # cleaner than checking with `if key in dict` first.
                direction = KEY_TO_DIRECTION.get(event.key)
                if direction is not None:
                    dx, dy = direction
                    # try_move handles the collision check internally.
                    # We could use the return value to play a "bump" sound
                    # on a failed move, but no sounds yet — ignore for now.
                    try_move(player, dungeon, dx, dy)

        # --- 2. Update game state ---
        # Still nothing here at the per-frame level. Movement happens
        # in response to events above, not on every frame.

        # --- 3. Draw everything ---
        # Drawing order: background -> dungeon -> character.
        # The character must be drawn AFTER the dungeon so it appears on top.
        screen.fill(COLOR_BACKGROUND)
        draw_dungeon(screen, dungeon, offset_x, offset_y)
        draw_character(screen, player, offset_x, offset_y)
        pygame.display.flip()

        # --- 4. Tick the clock ---
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()