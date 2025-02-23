from math import cos, pi, radians, sin, sqrt

from .conf import conf


class Particle:
    """Particle Man."""

    def __init__(self, x, y, mass, speed, angle):
        """Construct."""
        self.x = x
        self.y = y
        self.mass = mass
        self.speed = speed
        self.angle = angle

        self.radius = sqrt(self.mass) * conf["scale-factor"]

        self.update_angle(angle)

    def update_angle(self, angle):
        """Update our angle."""
        self.angle = angle
        self.update_increments()

    def update_increments(self):
        """Update speed."""
        self.increments = [
            increment * self.speed for increment in increments(self.angle)
        ]

    def move(self):
        """Move."""
        self.x += self.increments[0]
        self.y += self.increments[1]

    def draw(self, ctx):
        """Draw."""
        ctx.rgb(255, 0, 0)
        ctx.arc(
            self.x,
            self.y,
            self.radius,
            0,
            2 * pi,
            True,  # noqa: FBT003
        )
        ctx.fill()


def increments(angle):
    """Work out `dx` and `dy` for `angle`."""
    return (
        round(cos(radians(angle)), 10),
        round(-sin(radians(angle)), 10),
    )
