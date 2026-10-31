"""CalculiX analysis of a form-found shell: static, modal and linear buckling.

ShellBench's CalculiX wrapper (floor-r2) is not tagged yet, and ShellForm
never runs untagged ShellBench code (stop-loss rule). Until floor-r2 is
tagged, this module writes and reads its own decks. It is replaced by, or
cross-checked against, floor-r2 once that tag exists.

Mesh: the force density grid (odd n per side) is cut into 8-node S8R shell
elements, each covering a 3 x 3 patch of grid nodes (the centre node unused).
Units: SI (m, N, kg, Pa).
"""

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class FEResult:
    """Results of one CalculiX run.

    Attributes:
        max_disp_m: Largest displacement magnitude in the static step [m].
        reaction_n: Sum of support reactions in the static step, (fx, fy, fz) [N].
            CalculiX leaves out of RF any load lumped directly onto a
            supported node, so with edge supports this sum is less than the
            weight; with corner supports it equals the weight (checked by test).
        weight_n: Self-weight applied, from density, g, thickness and area [N].
        periods_s: Natural periods, longest first [s].
        buckling_factors: Linear buckling load factors under the static load.
    """

    max_disp_m: float
    reaction_n: np.ndarray
    weight_n: float
    periods_s: np.ndarray
    buckling_factors: np.ndarray


def find_ccx():
    """Return the CalculiX executable path, or None if it is not installed."""
    return shutil.which("ccx")


def s8r_elements(n):
    """Return S8R connectivity (CalculiX node order, 1-based) for an n x n grid.

    Args:
        n: Grid nodes per side; must be odd.

    Returns:
        Integer array, shape ((n-1)/2 squared, 8).
    """
    if n % 2 == 0:
        raise ValueError("S8R meshing needs an odd number of grid nodes per side")

    def nid(i, j):
        return j * n + i + 1

    els = []
    for J in range(0, n - 1, 2):
        for I in range(0, n - 1, 2):
            els.append([nid(I, J), nid(I + 2, J), nid(I + 2, J + 2), nid(I, J + 2),
                        nid(I + 1, J), nid(I + 2, J + 1), nid(I + 1, J + 2), nid(I, J + 1)])
    return np.array(els)


def surface_area(xyz, n):
    """Return the area of the grid surface from its triangles [m2]."""
    p = xyz.reshape(n, n, 3)
    a, b, c, d = p[:-1, :-1], p[:-1, 1:], p[1:, 1:], p[1:, :-1]
    t1 = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=-1)
    t2 = 0.5 * np.linalg.norm(np.cross(c - a, d - a), axis=-1)
    return float((t1 + t2).sum())


def write_deck(xyz, n, fixed, thickness_m, e_pa, nu, density_kg_m3,
               g=9.81, n_modes=3, n_buckle=2):
    """Return the CalculiX input deck text for one shell.

    Args:
        xyz: Grid nodes, shape (n*n, 3) [m].
        n: Grid nodes per side (odd).
        fixed: 0-based indices of pinned nodes (translations fixed).
        thickness_m: Uniform shell thickness [m].
        e_pa, nu: Young's modulus [Pa] and Poisson's ratio [-].
        density_kg_m3: Mass density [kg/m3].
        g: Gravitational acceleration [m/s2].
        n_modes, n_buckle: Number of modes and buckling factors requested.
    """
    els = s8r_elements(n)
    used = np.unique(els)
    lines = ["*NODE"]
    lines += [f"{k},{xyz[k-1,0]:.9e},{xyz[k-1,1]:.9e},{xyz[k-1,2]:.9e}" for k in used]
    lines.append("*ELEMENT,TYPE=S8R,ELSET=EALL")
    lines += [f"{e+1}," + ",".join(str(v) for v in row) for e, row in enumerate(els)]
    fixed_used = sorted(set(int(k) + 1 for k in fixed) & set(int(u) for u in used))
    lines.append("*NSET,NSET=FIX")
    lines += [",".join(str(v) for v in fixed_used[i:i + 16]) for i in range(0, len(fixed_used), 16)]
    lines.append("*NSET,NSET=NUSED")
    lines += [",".join(str(v) for v in used[i:i + 16]) for i in range(0, len(used), 16)]
    lines += ["*BOUNDARY", "FIX,1,3",
              "*MATERIAL,NAME=CONC", "*ELASTIC", f"{e_pa:.6e},{nu}",
              "*DENSITY", f"{density_kg_m3}",
              "*SHELL SECTION,ELSET=EALL,MATERIAL=CONC", f"{thickness_m}",
              "*STEP", "*STATIC", "*DLOAD", f"EALL,GRAV,{g},0,0,-1",
              "*NODE PRINT,NSET=FIX,TOTALS=ONLY", "RF",
              "*NODE PRINT,NSET=NUSED", "U", "*END STEP",
              "*STEP", "*FREQUENCY", f"{n_modes}", "*END STEP",
              "*STEP", "*BUCKLE", f"{n_buckle}", "*DLOAD", f"EALL,GRAV,{g},0,0,-1", "*END STEP"]
    return "\n".join(lines) + "\n"


_NUM = r"[-+]?\d*\.?\d+(?:[EeDd][-+]?\d+)?"


def parse_dat(text):
    """Return (max displacement, reaction totals, frequencies [Hz], buckling factors) from a .dat file."""
    steps = re.split(r"S T E P\s+\d+", text)
    static = steps[1] if len(steps) > 1 else text
    tot = re.search(r"total force \(fx,fy,fz\)[^\n]*\n\s*\n?\s*(" + _NUM + r")\s+(" + _NUM + r")\s+(" + _NUM + r")", static)
    reaction = np.array([float(tot.group(k)) for k in (1, 2, 3)]) if tot else np.full(3, np.nan)
    disp_block = static.split("displacements", 1)[1] if "displacements" in static else ""
    rows = re.findall(r"^\s*\d+\s+(" + _NUM + r")\s+(" + _NUM + r")\s+(" + _NUM + r")\s*$", disp_block, re.M)
    u = np.array(rows, dtype=float) if rows else np.zeros((1, 3))
    freq = []
    m = re.search(r"E I G E N V A L U E   O U T P U T(.*?)(?:\n\s*\n\s*\n|P A R T I C)", text, re.S)
    if m:
        for row in re.findall(r"^\s*\d+\s+(" + _NUM + r")\s+(" + _NUM + r")\s+(" + _NUM + r")", m.group(1), re.M):
            freq.append(float(row[2]))
    buck = []
    b = re.search(r"B U C K L I N G   F A C T O R   O U T P U T(.*?)(?:E I G E N V A L U E    N U M B E R|$)", text, re.S)
    if b:
        buck = [float(v) for v in re.findall(r"^\s*\d+\s+(" + _NUM + r")\s*$", b.group(1), re.M)]
    return float(np.linalg.norm(u, axis=1).max()), reaction, np.array(freq), np.array(buck)


def analyse(xyz, n, fixed, thickness_m, e_pa, nu, density_kg_m3, g=9.81, workdir=None, ccx=None):
    """Run static, modal and buckling analyses of one shell in CalculiX.

    Args:
        xyz, n, fixed, thickness_m, e_pa, nu, density_kg_m3, g: As for :func:`write_deck`.
        workdir: Folder for the deck and outputs; a temporary folder if None.
        ccx: CalculiX executable; found on PATH if None.

    Returns:
        FEResult.

    Raises:
        RuntimeError: If CalculiX is missing or fails.
    """
    ccx = ccx or find_ccx()
    if ccx is None:
        raise RuntimeError("CalculiX (ccx) not found on PATH")
    work = Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix="shellform_"))
    work.mkdir(parents=True, exist_ok=True)
    (work / "shell.inp").write_text(write_deck(xyz, n, fixed, thickness_m, e_pa, nu, density_kg_m3, g))
    run = subprocess.run([ccx, "shell"], cwd=work, capture_output=True, text=True)
    dat = work / "shell.dat"
    if not dat.exists() or "Job finished" not in run.stdout:
        raise RuntimeError(f"CalculiX failed:\n{run.stdout[-2000:]}\n{run.stderr[-2000:]}")
    umax, reaction, freq, buck = parse_dat(dat.read_text())
    weight = density_kg_m3 * g * thickness_m * surface_area(xyz, n)
    periods = np.sort(1.0 / freq)[::-1] if len(freq) else np.array([])
    return FEResult(umax, reaction, weight, periods, buck)
