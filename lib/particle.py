from math import cos, pi, radians, sin, sqrt

try:
    from ..pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue
except ImportError:
    from pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue

from .conf import conf
from .vector import Vector


class Particle:
    """Particle Man."""

    def __init__(  # noqa: PLR0913
        self,
        x,
        y,
        mass,
        speed,
        angle,
        hue=1.0,
        annotate=False,  # noqa: FBT002
        fancy_bounce=False,  # noqa: FBT002
    ):
        """Construct."""
        self.mass = mass
        self.speed = speed
        self.angle = angle
        self.hue = hue
        self.colliding_counter = 0
        self.max_colliding_counter = conf["collision-halo"]["additional-radius"]
        self.annotate = annotate
        self.fancy_bounce = fancy_bounce

        self.position = Vector(x, y)
        self.radius = sqrt(self.mass) * conf["particles"]["scale-factor"]
        self.velocity = Vector(
            round(cos(radians(self.angle)), 10) * self.speed,
            round(-sin(radians(self.angle)), 10) * self.speed,
        )
        self.update_kinetic_energy()

    def update_kinetic_energy(self):
        """How much energy do we have?"""
        self.kinetic_energy = (
            0.5 * self.mass * self.velocity.magnitude * self.velocity.magnitude
        )

    def move(self):
        """Move."""
        if self.colliding_counter > 0:
            self.colliding_counter -= 1

        self.position += self.velocity
        self.edges()

    def draw(self, ctx):
        """Draw."""
        colour = rgb_from_hue(self.hue)

        layers = [
            (colour, 1.0, ctx.fill, 0),  # body
            (  # border
                (c * conf["border-darkening-factor"] for c in colour),
                1.0,
                ctx.stroke,
                0,
            ),
        ]
        if self.colliding_counter > 0 and self.fancy_bounce:
            layers[1] = (  # special border
                colour,
                conf["collision-halo"]["opacity"]
                * (self.colliding_counter / self.max_colliding_counter),
                ctx.stroke,
                self.colliding_counter,
            )

        for colour, opacity, method, extra_radius in layers:
            rgba = list(colour) + [opacity]
            ctx.rgba(*rgba)
            ctx.arc(
                self.position.x,
                self.position.y,
                self.radius + extra_radius,
                0,
                2 * pi,
                True,  # noqa: FBT003
            )
            method()

        if self.annotate:
            self.annotations(ctx)

    def annotations(self, ctx):  # pragma: no cover
        """Draw our K.E."""
        ctx.move_to(*self.position.coords)
        ctx.rgb(*rgb_from_hue(self.hue + 0.5))
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = 20
        ctx.text(f"{self.kinetic_energy:0.2f}")

    def collide(self, other, hue=1.0):
        """Crash into a particle."""
        impact_vector = other.position - self.position
        delta = impact_vector.magnitude

        if delta < (self.radius + other.radius):
            fix_overlap(self, other, delta, impact_vector.copy())

            delta = self.radius + other.radius
            impact_vector.set_magnitude(delta)

            total_mass = self.mass + other.mass
            velocity_diff = other.velocity - self.velocity
            numerator = velocity_diff.dot(impact_vector)
            denominator = total_mass * delta * delta

            for left, right, factor in (
                (self, other, 2),
                (other, self, -2),
            ):
                amend_velocity(
                    left, right, factor, numerator, denominator, impact_vector.copy()
                )

            for particle in (self, other):
                particle.update_kinetic_energy()
                particle.hue = hue
                particle.colliding_counter = self.max_colliding_counter

    def edges(self):
        """Interact at edge."""
        width = 120
        offset = width - self.radius

        for component in ["x", "y"]:
            if self.position[component] > offset:
                self.position[component] = offset
                self.velocity.invert(component)
                self.colliding_counter = self.max_colliding_counter

            if self.position[component] < -offset:
                self.position[component] = -offset
                self.velocity.invert(component)
                self.colliding_counter = self.max_colliding_counter


def fix_overlap(this, other, delta, direction):
    """Fix collision overlap."""
    overlap = delta - (this.radius + other.radius)
    direction.set_magnitude(overlap * 0.5)
    this.position += direction
    other.position -= direction


def amend_velocity(this, other, factor, numerator, denominator, delta_vector):  # noqa: PLR0913
    """Amend velocity."""
    delta_vector *= factor * other.mass * numerator / denominator
    this.velocity += delta_vector
