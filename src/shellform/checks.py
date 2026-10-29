"""Solver-independent checks for the seismic-aware form-finding (tests S2, S3).

These functions do not form-find. They check a form produced by any
force density solver (ShellBench floor-r1, extended in ShellForm), so the
same checks run unchanged when the pin moves to a new ShellBench tag.

Conventions: nodal coordinates xyz [m] are an (n, 3) array; edges are
(m, 2) node index pairs; q [N/m] is the force density of each edge; loads
[N] are an (n, 3) array; ``free`` lists the indices of unsupported nodes.
"""

import numpy as np


def nodal_residuals(xyz, edges, q, loads, free):
    """Return the out-of-balance force at every free node [N].

    At a free node i, equilibrium in a force density network is
    sum_j q_ij (x_j - x_i) + p_i = 0 (Schek 1974).

    Args:
        xyz: Nodal coordinates, shape (n, 3) [m].
        edges: Node index pairs, shape (m, 2).
        q: Force density per edge, shape (m,) [N/m].
        loads: Nodal loads, shape (n, 3) [N].
        free: Indices of the free nodes.

    Returns:
        Residual force vectors at the free nodes, shape (len(free), 3) [N].
    """
    xyz = np.asarray(xyz, dtype=float)
    edges = np.asarray(edges, dtype=int)
    q = np.asarray(q, dtype=float)
    force = np.array(loads, dtype=float, copy=True)
    vec = xyz[edges[:, 1]] - xyz[edges[:, 0]]
    edge_force = q[:, None] * vec
    np.add.at(force, edges[:, 0], edge_force)
    np.add.at(force, edges[:, 1], -edge_force)
    return force[np.asarray(free, dtype=int)]


def equilibrium_error(xyz, edges, q, loads, free):
    """Return the largest free-node residual relative to the largest load (test S2).

    Args:
        xyz, edges, q, loads, free: As for :func:`nodal_residuals`.

    Returns:
        max |residual| / max |load| [-]. Test S2 passes below 1e-9.

    Raises:
        ValueError: If every load is zero, because the ratio is undefined.
    """
    residual = np.linalg.norm(nodal_residuals(xyz, edges, q, loads, free), axis=1)
    load_scale = np.linalg.norm(np.asarray(loads, dtype=float), axis=1).max()
    if load_scale == 0.0:
        raise ValueError("all loads are zero; the relative residual is undefined")
    return float(residual.max() / load_scale)


def rotate_z(vectors, angle_rad):
    """Rotate points or vectors about the vertical z axis.

    Args:
        vectors: Array of shape (n, 3).
        angle_rad: Rotation angle, anticlockwise seen from above [rad].

    Returns:
        Rotated array, shape (n, 3).
    """
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    rot = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return np.asarray(vectors, dtype=float) @ rot.T


def rotation_error(solve, xyz_supports, loads, angle_rad):
    """Return the error of the rotation test (test S3).

    Rotating every load and every support about z by one angle must rotate
    the form by the same angle, because the force density equations are
    linear and isotropic in plan.

    Args:
        solve: Callable ``solve(xyz_supports, loads) -> xyz`` wrapping the
            form-finder under test, with connectivity and force densities
            fixed inside it.
        xyz_supports: Coordinates used for the support nodes, shape (n, 3)
            [m]; the solver reads only the support rows.
        loads: Nodal loads, shape (n, 3) [N].
        angle_rad: Rotation angle [rad].

    Returns:
        Largest node distance between the two forms, divided by the largest
        plan dimension of the form [-]. Test S3 passes below 1e-9.
    """
    base = solve(xyz_supports, loads)
    turned = solve(rotate_z(xyz_supports, angle_rad), rotate_z(loads, angle_rad))
    expected = rotate_z(base, angle_rad)
    size = np.ptp(base[:, :2], axis=0).max()
    return float(np.linalg.norm(turned - expected, axis=1).max() / size)
