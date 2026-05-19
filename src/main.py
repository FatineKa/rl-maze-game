"""
Hermes : A simple game engine using Pygame and Reinforcement Learning Algorithms.

This is the application launcher. It opens the Pygame window
and runs the main loop.
"""

import sys
import pygame


# Window settings
size_x = 800
size_y = 600
window_title = "Hermes"
FPS = 60

# Colors (R, G, B)
BACKGROUND_COLOR = (20, 20, 30)        # Dark blue-grey
TEXT_COLOR = (220, 200, 150)           # Warm gold 


def main():
    # Initialize all Pygame modules
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption(window_title)

    # Create a clock to control frame rate
    clock = pygame.time.Clock()

    # Load a default font and render the title text once
    # (rendering text every frame is wasteful — do it once, reuse)
    font = pygame.font.SysFont(None, 120)
    title_surface = font.render("HERMES", True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(size_x // 2, size_y // 2))

    # Main loop
    running = True
    while running:
        # --- Handle events (input, window close, etc.) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Draw everything ---
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_surface, title_rect)
        pygame.display.flip()

        # --- Control speed ---
        clock.tick(FPS)

    # Clean shutdown
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()