"""scripts/day03_one_shell.py — Day 3 CalculiX analysis of one shell.

Form-finds the baseline shell (10 m span, rise/span 0.15, gravity form) for
both support cases, then runs a CalculiX static (self-weight), frequency and
linear buckling analysis on each. Writes results/day03_one_shell.json.

Inputs and where they come from:
- E: ShellBench v0.0.1, shellbench.anchor_frame.E_KN_M2 (C40, spec X4).
- Poisson ratio and density: NOT in ShellBench v0.0.1. Placeholders marked
  [?] until a ShellBench tag provides them; results are a pipeline check,
  not design values.
- Corner shells: boundary force density set so the free edge insets by
  0.10 x span at mid-edge (decision D3-1 [J]).
- Thickness 0.08 m: a trial value for the solver check, not a sized design.
"""

import json
from pathlib import Path

import shellbench.anchor_frame as sb_frame

from shellform.fe import analyse, surface_area
from shellform.formfind import corner_network_for_inset, form_to_rise, square_network
from shellform.pin import SHELLBENCH_TAG, check_pin

ROOT = Path(__file__).resolve().parents[1]
SPAN_M, RISE_RATIO, N_GRID, THICKNESS_M = 10.0, 0.15, 21, 0.08
NU_PLACEHOLDER = 0.2          # [?] not from ShellBench v0.0.1
DENSITY_PLACEHOLDER = 2500.0  # [?] kg/m^3, not from ShellBench v0.0.1
CORNER_EDGE_INSET_RATIO = 0.10  # [J] free-edge mid inset / span, decision D3-1


def main() -> None:
    """Run both support cases and write the results file."""
    check_pin()
    e_pa = sb_frame.E_KN_M2 * 1.0e3
    out = {"shellbench_tag": SHELLBENCH_TAG,
           "inputs": {"span_m": SPAN_M, "rise_ratio": RISE_RATIO, "grid_n": N_GRID,
                      "thickness_m": THICKNESS_M, "e_pa": e_pa,
                      "e_source": f"ShellBench {SHELLBENCH_TAG} anchor_frame.E_KN_M2",
                      "nu": NU_PLACEHOLDER, "density_kg_m3": DENSITY_PLACEHOLDER,
                      "nu_density_status": "[?] placeholders, not from ShellBench"},
           "cases": {}}
    for supports in ("edges", "corners"):
        if supports == "edges":
            net = square_network(SPAN_M, N_GRID, "edges")
            xyz, qf = form_to_rise(net, RISE_RATIO * SPAN_M), 1.0
        else:
            net, xyz, qf = corner_network_for_inset(
                SPAN_M, N_GRID, RISE_RATIO * SPAN_M, CORNER_EDGE_INSET_RATIO)
        r = analyse(xyz, N_GRID, net.fixed, THICKNESS_M, e_pa, NU_PLACEHOLDER,
                    DENSITY_PLACEHOLDER, workdir=ROOT / "results" / "ccx" / f"day03_{supports}")
        out["cases"][supports] = {
            "boundary_q_factor": qf, "surface_area_m2": surface_area(xyz, N_GRID),
            "max_disp_m": r.max_disp_m, "span_over_disp": SPAN_M / r.max_disp_m,
            "weight_n": r.weight_n, "reaction_z_n": r.reaction_n[2],
            "reaction_over_weight": r.reaction_n[2] / r.weight_n,
            "periods_s": list(r.periods_s), "buckling_factors": list(r.buckling_factors)}
    path = ROOT / "results" / "day03_one_shell.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out["cases"], indent=2))


if __name__ == "__main__":
    main()
