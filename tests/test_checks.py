"""Tests for the S2/S3 check helpers, run against a small test-only solver.

``_toy_fdm`` is a minimal force density solver used only to exercise the
checks. It is not ShellForm's form-finder: the real one imports ShellBench
floor-r1 once that tag exists (docs/data_contract.md, section 2).
"""

import numpy as np
import pytest

from shellform.checks import equilibrium_error, nodal_residuals, rotate_z, rotation_error


def _grid(n=7, span=10.0):
    """Square n x n grid network with all boundary nodes supported."""
    xs = np.linspace(-span / 2, span / 2, n)
    xyz = np.array([[x, y, 0.0] for y in xs for x in xs])
    idx = lambda i, j: j * n + i
    edges = [(idx(i, j), idx(i + 1, j)) for j in range(n) for i in range(n - 1)]
    edges += [(idx(i, j), idx(i, j + 1)) for j in range(n - 1) for i in range(n)]
    fixed = [idx(i, j) for j in range(n) for i in range(n) if i in (0, n - 1) or j in (0, n - 1)]
    free = [k for k in range(n * n) if k not in fixed]
    return xyz, np.array(edges), free, fixed


def _toy_fdm(xyz_supports, loads, edges, q, free, fixed):
    """Solve D x_free = p_free - D_f x_fixed for all three coordinates (Schek 1974)."""
    n = len(xyz_supports)
    C = np.zeros((len(edges), n))
    C[np.arange(len(edges)), edges[:, 0]] = 1.0
    C[np.arange(len(edges)), edges[:, 1]] = -1.0
    Q = np.diag(q)
    Cf, Cx = C[:, free], C[:, fixed]
    D, Df = Cf.T @ Q @ Cf, Cf.T @ Q @ Cx
    xyz = np.array(xyz_supports, dtype=float, copy=True)
    xyz[free] = np.linalg.solve(D, np.asarray(loads, dtype=float)[free] - Df @ xyz[fixed])
    return xyz


@pytest.fixture
def net():
    xyz, edges, free, fixed = _grid()
    q = -np.full(len(edges), 10.0e3)  # compression [N/m]
    w = 5.0e3  # nodal weight [N]
    loads = np.zeros_like(xyz)
    loads[:, 2] = -w
    return xyz, edges, q, loads, free, fixed


def test_equilibrium_of_solved_form_is_machine_precision(net):
    xyz, edges, q, loads, free, fixed = net
    form = _toy_fdm(xyz, loads, edges, q, free, fixed)
    assert form[free, 2].min() > 0.0  # compression form stands up
    assert equilibrium_error(form, edges, q, loads, free) < 1e-9


def test_equilibrium_error_detects_a_moved_node(net):
    xyz, edges, q, loads, free, fixed = net
    form = _toy_fdm(xyz, loads, edges, q, free, fixed)
    form[free[0], 2] += 0.01
    assert equilibrium_error(form, edges, q, loads, free) > 1e-3


def test_residual_of_single_node_by_hand():
    xyz = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
    edges = np.array([[0, 1], [0, 2]])
    q = np.array([3.0, 4.0])
    loads = np.zeros((3, 3))
    # Node 0: 3*(1,0,0) + 4*(0,2,0) = (3, 8, 0)
    assert np.allclose(nodal_residuals(xyz, edges, q, loads, [0]), [[3.0, 8.0, 0.0]])


def test_rotation_test_passes_with_lateral_load(net):
    xyz, edges, q, loads, free, fixed = net
    lateral = loads.copy()
    lateral[:, 0] = 0.3 * 5.0e3  # 0.3 g in x on every node
    solve = lambda sup, p: _toy_fdm(sup, p, edges, q, free, fixed)
    for angle in (0.3, np.pi / 2, 2.0):
        assert rotation_error(solve, xyz, lateral, angle) < 1e-9


def test_rotate_z_quarter_turn():
    assert np.allclose(rotate_z([[1.0, 0.0, 2.0]], np.pi / 2), [[0.0, 1.0, 2.0]])


def test_uniform_lateral_acceleration_shears_the_gravity_form(net):
    """With nodal loads fixed and supports at z = 0, adding p_x = a w to every
    node gives x = x_gravity - a z_gravity: the seismic form is a horizontal
    shear of the gravity form (notes/michiels2017.md, finding F1)."""
    xyz, edges, q, loads, free, fixed = net
    a = 0.3
    grav = _toy_fdm(xyz, loads, edges, q, free, fixed)
    lateral = loads.copy()
    lateral[:, 0] = -a * loads[:, 2]
    seis = _toy_fdm(xyz, lateral, edges, q, free, fixed)
    assert np.allclose(seis[:, 0], grav[:, 0] - a * grav[:, 2], atol=1e-12)
    assert np.allclose(seis[:, 1:], grav[:, 1:], atol=1e-12)
