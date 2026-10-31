"""Tests for ShellForm's 3D force density solver."""

import numpy as np
import pytest

from shellform.checks import equilibrium_error, rotation_error
from shellform.formfind import Network, form_to_rise, plan_loads, solve, square_network


def test_chain_under_uniform_nodal_load_is_an_exact_parabola():
    """A straight chain is the 2D case floor-r1 solves; force density gives
    the parabola exactly at the nodes: z_i = w x_i (L - x_i) / (2 |q| h)."""
    n, L, w, q = 21, 6.0, 2.0, -5.0
    x = np.linspace(0.0, L, n)
    xyz = np.column_stack([x, np.zeros(n), np.zeros(n)])
    edges = np.column_stack([np.arange(n - 1), np.arange(1, n)])
    net = Network(xyz, edges, np.full(n - 1, q), np.array([0, n - 1]), np.arange(1, n - 1),
                  np.zeros(n - 1, bool))
    form = solve(net, plan_loads(net, w_node=w))
    h = L / (n - 1)
    assert np.allclose(form[:, 2], w * x * (L - x) / (2 * abs(q) * h**2), atol=1e-12)


def test_edge_supported_square_matches_membrane_centre_value():
    """Uniform q on an edge-supported square is a discrete membrane:
    z_centre -> 0.0737 p a^2 / T, with T = |q| (edge force |q| h per spacing h) as the mesh is refined (Timoshenko,
    Theory of Plates and Shells, membrane analogy [check])."""
    a, n = 10.0, 61
    net = square_network(a, n, "edges", q=-1.0)
    h = a / (n - 1)
    form = solve(net, plan_loads(net, w_node=h * h))  # p = 1 N/m2
    zc = form[:, 2].max()
    assert zc == pytest.approx(0.0737 * a**2 / 1.0, rel=0.01)


@pytest.mark.parametrize("supports, factor", [("edges", 1.0), ("corners", 4.0)])
def test_form_has_target_rise_and_is_in_equilibrium(supports, factor):
    net = square_network(10.0, 15, supports, q_boundary_factor=factor)
    form = form_to_rise(net, 1.5)
    assert form[:, 2].max() == pytest.approx(1.5, rel=1e-12)
    assert equilibrium_error(form, net.edges, net.q, plan_loads(net), net.free) < 1e-9


def test_S1_zero_lateral_load_returns_the_gravity_form():
    net = square_network(10.0, 15, "corners", q_boundary_factor=4.0)
    grav = form_to_rise(net, 1.5)
    net2 = square_network(10.0, 15, "corners", q_boundary_factor=4.0)
    seis0 = form_to_rise(net2, 1.5, sa_x=0.0)
    assert np.array_equal(grav, seis0)


def test_S2_equilibrium_with_lateral_load():
    net = square_network(20.0, 21, "edges")
    form = form_to_rise(net, 3.0, sa_x=0.4, sa_y=0.2)
    loads = plan_loads(net, sa_x=0.4, sa_y=0.2)
    assert equilibrium_error(form, net.edges, net.q, loads, net.free) < 1e-9


def test_S3_rotation_on_the_shell_solver():
    net = square_network(10.0, 13, "corners", q_boundary_factor=4.0)
    form_to_rise(net, 1.5)  # fixes q
    loads = plan_loads(net, sa_x=0.3)

    def run(sup_xyz, p):
        trial = Network(sup_xyz, net.edges, net.q, net.fixed, net.free, net.boundary_edge)
        return solve(trial, p)

    for angle in (0.4, np.pi / 2):
        assert rotation_error(run, net.xyz, loads, angle) < 1e-9


def test_F1_shell_seismic_form_is_shear_of_gravity_form():
    net = square_network(10.0, 15, "edges")
    grav = form_to_rise(net, 1.5)
    seis = solve(net, plan_loads(net, sa_x=0.3))
    assert np.allclose(seis[:, 0], grav[:, 0] - 0.3 * grav[:, 2], atol=1e-12)


def test_corner_inset_search_hits_target():
    """The boundary-factor search gives the requested free-edge inset."""
    from shellform.formfind import corner_network_for_inset, edge_inset
    net, xyz, f = corner_network_for_inset(10.0, 11, 1.5, 0.10)
    plan = square_network(10.0, 11, "corners").xyz
    assert edge_inset(xyz, plan, 10.0) / 10.0 == pytest.approx(0.10, abs=1e-3)
    assert xyz[:, 2].max() == pytest.approx(1.5)
    assert f > 1.0
