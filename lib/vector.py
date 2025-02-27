# https://www.reddit.com/r/learnpython/comments/l33xe9/comment/gkbbysq/
from math import sqrt


class Vector:
    """A Vector."""

    def __init__(self, x, y):
        """Construct."""
        self.x = x
        self.y = y

    def __add__(self, other):
        """Add them."""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract them."""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiply."""
        return Vector(other * self.x, other * self.y)

    def dot(self, other):
        """Dot.product."""
        return self.x * other.x + self.y * other.y

    def __getitem__(self, key):
        """`v["x"]`."""
        if key == "x":
            return self.x
        if key == "y":  # noqa: RET503
            return self.y

    def __setitem__(self, key, value):
        """`v["y"] = 1`."""
        if key == "x":
            self.x = value
        if key == "y":
            self.y = value

    @property
    def magnitude(self):
        """Magnitude."""
        return sqrt(self.x**2 + self.y**2)

    def set_magnitude(self, new_magnitude):
        """Set the magnitude."""
        current_magnitude = self.magnitude
        self.x = self.x * (new_magnitude / current_magnitude)
        self.y = self.y * (new_magnitude / current_magnitude)

    @property
    def coords(self):
        """Get x and y."""
        return (self.x, self.y)

    def copy(self):
        """Copy ourself."""
        return Vector(self.x, self.y)

    def invert(self, component):
        """Invert a component."""
        self[component] *= -1
