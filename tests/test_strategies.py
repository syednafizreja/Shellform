"""Tests for the strategies and the thrust-envelope thickness."""

import numpy as np
import pytest

from shellform.formfind import square_network
from shellform.strategies import envelope_thickness, strategy_forms


@pytest.fixture(params=[("edges", 1.0), ("corners", 4.0)])
def forms(request):
    supports, factor = request.param
    def make(sa):
        net = square_network(10.0, 21, supports, q_boundary_factor=factor)
        return strategy_forms(net, 1.5, sa)
    return make


def test_S1_strategy_2_at_zero_sa_is_the_gravity_form(forms):
    grav, s1, s2 = forms(0.0)
    assert np.array_equal(s2, grav)
    assert envelope_thickness(grav, grav, 0.0) < 1e-5  # lam found to 1e-6


def test_seismic_mid_surface_keeps_rise_and_supports(forms):
    grav, _, s2 = forms(0.3)
    assert s2[:, 2].max() == pytest.approx(1.5, rel=1e-9)
    assert np.allclose(s2[:, :2], grav[:, :2])


def test_envelope_grows_with_sa_for_both_strategies(forms):
    """Which strategy needs less is a result, not a test; only monotonicity is tested."""
    prev = [0.0, 0.0]
    for sa in (0.1, 0.3, 0.5):
        grav, s1, s2 = forms(sa)
        t = [envelope_thickness(s1, grav, sa), envelope_thickness(s2, grav, sa)]
        assert t[0] > prev[0] and t[1] > prev[1]
        prev = t
