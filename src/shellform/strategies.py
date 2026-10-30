"""The two form strategies and the thrust-envelope thickness (pre-registration section 2).

A thrust surface T(d, lam) for shaking direction d is the gravity form G
scaled vertically by lam and moved horizontally by -Sa * lam * z_G * d
(finding F1). lam is free because the horizontal thrust of a funicular is
statically free. Gaps are measured vertically at the plan points of the
mid-surface and turned into a thickness normal to the mid-surface by the
cosine of its slope (first order in the gap) [J]; outside a thrust
surface's plan the nearest value is used [J].
"""

import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from scipy.optimize import minimize_scalar

from shellform.formfind import form_to_rise

DIRECTIONS = ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0))
LAMBDA_BOUNDS = (0.2, 5.0)


def thrust_surface(gravity_xyz, sa_g, direction, lam):
    """Return the nodes of T(d, lam) (pre-registration section 2).

    Args:
        gravity_xyz: Gravity form G, shape (n, 3) [m].
        sa_g: Horizontal acceleration [g].
        direction: Unit plan vector (dx, dy).
        lam: Vertical scale of the thrust surface [-].

    Returns:
        Nodal coordinates, shape (n, 3) [m].
    """
    z = lam * gravity_xyz[:, 2]
    out = gravity_xyz.copy()
    out[:, 0] -= sa_g * z * direction[0]
    out[:, 1] -= sa_g * z * direction[1]
    out[:, 2] = z
    return out


def _heights_at(surface_xyz, plan_xy):
    """Interpolate a surface's height at plan points (nearest outside its plan)."""
    lin = LinearNDInterpolator(surface_xyz[:, :2], surface_xyz[:, 2])
    z = lin(plan_xy)
    out = np.isnan(z)
    if out.any():
        z[out] = NearestNDInterpolator(surface_xyz[:, :2], surface_xyz[:, 2])(plan_xy[out])
    return z


def _cos_slope(mid_xyz):
    """Return cos(slope) of a surface given on a square n x n grid of nodes."""
    n = int(round(np.sqrt(len(mid_xyz))))
    x = mid_xyz[:n, 0]
    zz = mid_xyz[:, 2].reshape(n, n)
    dz_dy, dz_dx = np.gradient(zz, x, x)
    return (1.0 / np.sqrt(1.0 + dz_dx**2 + dz_dy**2)).ravel()


def direction_gap(mid_xyz, gravity_xyz, sa_g, direction):
    """Return (smallest worst normal gap [m], lam) for one shaking direction."""
    plan = mid_xyz[:, :2]
    cos = _cos_slope(mid_xyz)

    def worst(lam):
        z_t = _heights_at(thrust_surface(gravity_xyz, sa_g, direction, lam), plan)
        return (np.abs(mid_xyz[:, 2] - z_t) * cos).max()

    res = minimize_scalar(worst, bounds=LAMBDA_BOUNDS, method="bounded",
                          options={"xatol": 1e-6})
    return float(res.fun), float(res.x)


def envelope_thickness(mid_xyz, gravity_xyz, sa_g):
    """Return t_env [m]: twice the worst gap over the four directions.

    Args:
        mid_xyz: Mid-surface M, shape (n, 3) [m].
        gravity_xyz: Gravity form G of the force density pattern, shape (n, 3) [m].
        sa_g: Horizontal acceleration [g].

    Returns:
        Envelope thickness normal to the mid-surface [m].
    """
    return 2.0 * max(direction_gap(mid_xyz, gravity_xyz, sa_g, d)[0] for d in DIRECTIONS)


def seismic_mid_surface(gravity_xyz, sa_g, rise_m, iterations=20):
    """Return strategy 2's mid-surface: the midrange of the four thrust surfaces.

    At each plan point the mid-surface lies halfway between the highest and
    the lowest of T(+x), T(-x), T(+y), T(-y): the centre of the band that
    must hold all four, like the middle of Michiels' double layer [J].

    lam is set so the mean surface has the target rise (fixed-point
    iteration). At sa_g = 0 this returns the gravity form exactly.

    Args:
        gravity_xyz: Gravity form G with rise rise_m, shape (n, 3) [m].
        sa_g: Design horizontal acceleration [g].
        rise_m: Target rise of the mid-surface [m].
        iterations: Fixed-point iterations on lam.

    Returns:
        Mid-surface nodes on G's plan points, shape (n, 3) [m].
    """
    if sa_g == 0.0:
        return gravity_xyz.copy()
    plan = gravity_xyz[:, :2]
    lam = 1.0
    for _ in range(iterations):
        zs = np.array([_heights_at(thrust_surface(gravity_xyz, sa_g, d, lam), plan)
                       for d in DIRECTIONS])
        z = 0.5 * (zs.max(axis=0) + zs.min(axis=0))
        lam *= rise_m / z.max()
    mid = gravity_xyz.copy()
    mid[:, 2] = z * rise_m / z.max()
    return mid


def strategy_forms(net, rise_m, sa_g):
    """Return (gravity form, strategy 1 mid-surface, strategy 2 mid-surface).

    Args:
        net: A Network from formfind.square_network (q is scaled in place).
        rise_m: Target rise [m].
        sa_g: Design horizontal acceleration [g].
    """
    grav = form_to_rise(net, rise_m)
    return grav, grav.copy(), seismic_mid_surface(grav, sa_g, rise_m)
