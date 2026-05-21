"""
The Character class — anything that can move through the dungeon.

This includes the player and (eventually) NPCs controlled by RL agents.

"""


class Character:
    """
    A character occupying a single tile of the dungeon.

    Attributes:
        x: column index in the grid (0 is leftmost)
        y: row index in the grid (0 is topmost)

    Both x and y are *grid coordinates*, not pixel coordinates.
    Translating grid->pixel happens only when drawing. Keeping the
    game logic in grid space means we can change tile sizes or even
    render-style without rewriting movement logic.
    """

    def __init__(self, x, y):
        # Starting position. We don't validate here that (x, y) is a
        # walkable tile — that's the caller's responsibility. The Character
        # class is intentionally dumb; it just holds state. Logic about
        # what's valid lives in the physics module.
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """
        Move by (dx, dy) tiles.

        """
        self.x += dx
        self.y += dy