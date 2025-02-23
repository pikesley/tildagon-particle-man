from math import pi
from unittest.mock import MagicMock

from lib.particle import Particle


def test_particle():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)

    assert part.x == 0
    assert part.radius == 20


def test_moving():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=10, angle=90)

    part.move()
    part.move()

    assert part.x == 0
    assert part.y == -20


def test_drawing():
    """Test."""
    part = Particle(x=0, y=0, mass=1, speed=1, angle=90)
    mock_ctx = MagicMock()

    part.draw(mock_ctx)
    mock_ctx.arc.assert_called_with(0, 0, 20.0, 0, 2 * pi, True)  # noqa: FBT003
