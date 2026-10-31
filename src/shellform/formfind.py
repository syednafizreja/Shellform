"""3D force density form-finding for square-plan shells (ShellForm's own solver).

ShellBench floor-r1 form-finds a 2D vault curve. ShellForm's shells are
doubly curved on square plans, so ShellForm solves the 3D force density
equations itself (Schek 1974). Lateral loads follow Michiels &
Adriaenssens: a horizontal acceleration Sa (in g) acting on the same
nodal weights as gravity (notes/michiels2017.md).

Sign convention: z is up; gravity loads are negative; force densities are
negative for compression, so the compression form stands above the
supports at z = 0.
"""

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


@dataclass
class Network:
    """A pin-jointed network on a square plan.

    Attributes:
        xyz: Nodal coordinates, shape (n, 3) [m]; support rows are used as given.
        edges: Node index pairs, shape (m, 2).
        q: Force density per edge, shape (m,) [N/m]; negative = compression.
        fixed: Indices of supported nodes.
        free: Indices of free nodes.
        boundary_edge: True for edges along the plan boundary, shape (m,).
    """

    xyz: np.ndarray
    edges: np.ndarray
    q: np.ndarray
    fixed: np.ndarray
    free: np.ndarray
    boundary_edge: np.ndarray


def square_network(span_m, n, supports, q=-1.0, q_boundary_factor=1.0):
    """Return an n x n grid network on a square plan centred at the origin.

    Args:
        span_m: Side length of the square plan [m].
        n: Nodes per side (n >= 3).
        supports: "edges" (every boundary node pinned) or "corners" (the four
            corner nodes pinned; the boundary acts as an edge arch).
        q: Force density of interior edges [N/m]; negative = compression.
        q_boundary_factor: Multiplier on q for boundary edges. With corner
            supports the free edges need a larger value to stay up [J].

    Returns:
        A Network with z = 0 everywhere.
    """
    if n < 3:
        raise ValueError("n must be at least 3")
    if supports not in ("edges", "corners"):
        raise ValueError("supports must be 'edges' or 'corners'")
    s = np.linspace(-span_m / 2, span_m / 2, n)
    xyz = np.array([[x, y, 0.0] for y in s for x in s])

    def idx(i, j):
        return j * n + i

    edges, boundary = [], []
    for j in range(n):
        for i in range(n - 1):
            edges.append((idx(i, j), idx(i + 1, j)))
            boundary.append(j in (0, n - 1))
    for j in range(n - 1):
        for i in range(n):
            edges.append((idx(i, j), idx(i, j + 1)))
            boundary.append(i in (0, n - 1))
    edges = np.array(edges)
    boundary = np.array(boundary)
    qv = np.where(boundary, q * q_boundary_factor, q).astype(float)

    on_edge = [idx(i, j) for j in range(n) for i in range(n) if i in (0, n - 1) or j in (0, n - 1)]
    corners = [idx(0, 0), idx(n - 1, 0), idx(0, n - 1), idx(n - 1, n - 1)]
    fixed = np.array(sorted(on_edge if supports == "edges" else corners))
    free = np.setdiff1d(np.arange(n * n), fixed)
    return Network(xyz, edges, qv, fixed, free, boundary)


def solve(net, loads):
    """Return the equilibrium form of a network under nodal loads.

    Solves D x_free = p_free - D_f x_fixed for x, y and z (Schek 1974),
    with D = C_f^T Q C_f and D_f = C_f^T Q C_x.

    Args:
        net: The Network (support coordinates are taken from net.xyz).
        loads: Nodal loads, shape (n, 3) [N].

    Returns:
        Nodal coordinates of the form, shape (n, 3) [m].
    """
    m, n = len(net.edges), len(net.xyz)
    rows = np.repeat(np.arange(m), 2)
    cols = net.edges.ravel()
    vals = np.tile([1.0, -1.0], m)
    C = sp.csr_matrix((vals, (rows, cols)), shape=(m, n))
    Q = sp.diags(net.q)
    Cf, Cx = C[:, net.free], C[:, net.fixed]
    D = (Cf.T @ Q @ Cf).tocsc()
    Df = Cf.T @ Q @ Cx
    rhs = np.asarray(loads, dtype=float)[net.free] - Df @ net.xyz[net.fixed]
    xyz = net.xyz.copy()
    xyz[net.free] = spla.splu(D).solve(rhs)
    return xyz


def plan_loads(net, w_node=1.0, sa_x=0.0, sa_y=0.0):
    """Return nodal loads: weight w down, plus Sa x weight horizontally.

    Args:
        net: The Network.
        w_node: Weight per node [N]. The form does not depend on its scale
            once the rise is fixed (see :func:`form_to_rise`).
        sa_x, sa_y: Horizontal accelerations in x and y [g].

    Returns:
        Loads, shape (n, 3) [N].
    """
    loads = np.zeros_like(net.xyz)
    loads[:, 0] = sa_x * w_node
    loads[:, 1] = sa_y * w_node
    loads[:, 2] = -w_node
    return loads


def form_to_rise(net, rise_m, sa_x=0.0, sa_y=0.0):
    """Return the form whose gravity-only rise equals rise_m.

    The force densities are scaled once, from the gravity-only solution, so
    the gravity form has exactly rise_m above the supports. The same scaled
    force densities are used with the lateral load, so the seismic form is
    the gravity form sheared by -Sa z (finding F1).

    Args:
        net: The Network; its q is scaled in place.
        rise_m: Target rise of the gravity form [m].
        sa_x, sa_y: Horizontal accelerations [g].

    Returns:
        Nodal coordinates of the form, shape (n, 3) [m].
    """
    z0 = solve(net, plan_loads(net))[:, 2].max()
    if z0 <= 0.0:
        raise ValueError("form does not stand up; use negative (compression) q")
    net.q = net.q * (z0 / rise_m)
    return solve(net, plan_loads(net, sa_x=sa_x, sa_y=sa_y))


def edge_inset(xyz_form, xyz_plan, span_m):
    """Return the plan inset of the free edge at its midpoint [m].

    Args:
        xyz_form: Form-found coordinates, shape (n, 3) [m].
        xyz_plan: Starting plan grid of the same network, shape (n, 3) [m].
        span_m: Plan side length [m].

    Returns:
        How far the mid-edge node on the y = -span/2 side has moved inward.
    """
    k = np.argmin(np.hypot(xyz_plan[:, 0], xyz_plan[:, 1] + span_m / 2.0))
    return xyz_form[k, 1] + span_m / 2.0


def corner_network_for_inset(span_m, n, rise_m, inset_ratio, lo=1.0, hi=200.0, tol=1e-3):
    """Return a corner-supported network whose free edge insets by inset_ratio * span.

    Free edges of a corner-supported net pull in towards the centre; a higher
    boundary force density keeps them closer to the plan square. This finds the
    boundary factor by bisection (the inset falls as the factor rises).

    Args:
        span_m: Plan side length [m].
        n: Nodes per side.
        rise_m: Target gravity rise [m].
        inset_ratio: Target mid-edge inset divided by span [-].
        lo, hi: Bracket for the boundary factor [-].
        tol: Tolerance on the inset ratio [-].

    Returns:
        (network with q scaled to the rise, form coordinates, boundary factor).
    """
    def trial(f):
        net = square_network(span_m, n, "corners", q_boundary_factor=f)
        plan = net.xyz.copy()
        xyz = form_to_rise(net, rise_m)
        return net, xyz, edge_inset(xyz, plan, span_m) / span_m

    for _ in range(60):
        mid = np.sqrt(lo * hi)
        net, xyz, r = trial(mid)
        if abs(r - inset_ratio) < tol:
            break
        lo, hi = (mid, hi) if r > inset_ratio else (lo, mid)
    return net, xyz, mid
