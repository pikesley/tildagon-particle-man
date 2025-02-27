from lib.vector import Vector


def test_vector():
    """Test."""
    vec_a = Vector(10, 20)
    vec_b = Vector(-20, 80)

    assert vec_a.magnitude == 22.360679774997898

    assert (vec_a + vec_b).coords == (-10, 100)
    assert (vec_a - vec_b).coords == (30, -60)
