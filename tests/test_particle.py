from math import pi
from unittest.mock import MagicMock

from lib.conf import conf
from lib.particle import Particle


def test_particle():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)

    assert part.position.x == 0
    assert part.radius == 1 * conf["particles"]["scale-factor"]


def test_moving():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=10, angle=90)

    part.move()
    part.move()

    assert part.position.x == 0
    assert part.position.y == -20


def test_drawing():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)
    mock_ctx = MagicMock()

    part.draw(mock_ctx)
    mock_ctx.arc.assert_called_with(
        0,
        0,
        1 * conf["particles"]["scale-factor"],
        0,
        2 * pi,
        True,  # noqa: FBT003
    )


def test_annotations():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)
    part.annotate = True
    mock_ctx = MagicMock()

    part.draw(mock_ctx)
    mock_ctx.text.assert_called_with("0.50")


def test_kinetic_energy():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)

    assert part.kinetic_energy == 0.5


def test_straight_collision():
    """Test."""
    part_a = Particle(x=0, y=0, mass=1, speed=5, angle=0)
    part_b = Particle(x=15, y=0, mass=1, speed=5, angle=180)

    assert part_a.velocity.coords == (5.0, 0.0)
    assert part_b.velocity.coords == (-5.0, 0.0)

    part_a.collide(part_b)
    assert part_a.velocity.coords == (5.0, 0.0)
    assert part_b.velocity.coords == (-5.0, 0.0)

    part_a.move()
    part_a.collide(part_b)
    assert part_a.velocity.coords == (-5.0, 0.0)
    assert part_b.velocity.coords == (5.0, 0.0)


def test_angled_collision():
    """Test."""
    part_a = Particle(x=0, y=0, mass=2, speed=1, angle=19)
    part_b = Particle(x=20, y=-20, mass=2, speed=7, angle=225)

    assert part_a.velocity.coords == (0.9455185756, -0.3255681545)
    assert part_b.velocity.coords == (-4.9497474684, 4.9497474684)

    part_a.collide(part_b)
    assert part_a.velocity.coords == (0.9455185756, -0.3255681545)
    assert part_b.velocity.coords == (-4.9497474684, 4.9497474684)

    part_a.move()
    part_b.move()
    part_a.move()
    part_b.move()
    part_a.collide(part_b)

    assert part_a.velocity.coords == (-4.201991748821676, 5.599386269210291)
    assert part_b.velocity.coords == (0.19776285602167576, -0.9752069553102913)


def test_edge_bouncing():
    """Test."""
    part_a = Particle(x=100, y=0, mass=2, speed=10, angle=5)
    assert part_a.velocity.coords == (9.961946981, -0.8715574269999999)
    part_a.move()
    part_a.move()
    assert part_a.velocity.coords == (-9.961946981, -0.8715574269999999)

    part_a = Particle(x=-110, y=0, mass=2, speed=10, angle=190)
    assert part_a.velocity.coords == (-9.84807753, 1.7364817769999998)
    part_a.move()
    assert part_a.velocity.coords == (9.84807753, 1.7364817769999998)

    part_a = Particle(x=0, y=110, mass=2, speed=10, angle=265)
    assert part_a.velocity.coords == (-0.8715574269999999, 9.961946981)
    part_a.move()
    assert part_a.velocity.coords == (-0.8715574269999999, -9.961946981)

    part_a = Particle(x=0, y=-110, mass=2, speed=10, angle=50)
    assert part_a.velocity.coords == (6.427876097, -7.660444431)
    part_a.move()
    assert part_a.velocity.coords == (6.427876097, 7.660444431)
