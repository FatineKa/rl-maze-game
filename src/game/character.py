"""
Character class — used for both the player and the RL agent.
"""


class Character:
    """
    Holds the position of a character on the grid.

    x and y are grid coordinates, not pixels.
    Pixel conversion happens only in the renderer.
    """

    def __init__(self, x, y):
        # no walkability check here — that's the caller's job
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move by (dx, dy) tiles."""
        self.x += dx
        self.y += dy
