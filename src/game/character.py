"""
Character class for tracking grid position.
"""

class Character:
    """
    Tracks the grid coordinates of the player or agent.
    Coordinate-to-pixel conversion is handled by the renderer.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Update grid position by dx, dy."""
        self.x += dx
        self.y += dy
