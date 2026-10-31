# Day 3: one shell through CalculiX (31 Oct 2026)

ShellBench tag: v0.0.1. Script: `scripts/day03_one_shell.py`. Results: `results/day03_one_shell.json`. CalculiX 2.21 (cloud); the author's laptop has 2.23.

## Inputs

- Form: gravity strategy, 10 m square plan, rise 1.5 m (rise/span 0.15), 21 x 21 nodes, 100 S8R elements (3 x 3 node patches).
- Thickness 0.08 m: a trial value for the pipeline check. It is not a sized design.
- E = 3.25e10 Pa from ShellBench v0.0.1 (`shellbench.anchor_frame.E_KN_M2`, C40, spec X4).
- Poisson's ratio 0.2 and density 2500 kg/m³ are placeholders [?]. ShellBench v0.0.1 has neither. They must come from a ShellBench tag before the design runs.
- Load: self-weight only (GRAV, g = 9.81 m/s²). Steps: static, frequency (3 modes), linear buckling (2 modes).

## Results

| | Edge-supported | Corner-supported |
|---|---|---|
| Surface area | 106.9 m² | 77.0 m² |
| Max displacement | 0.048 mm (L/208 500) | 1.74 mm (L/5 760) |
| First period T1 | 0.022 s | 0.139 s |
| First buckling factor λ | 680 | 11.8 |
| Vertical reaction / weight | 0.927 (see note) | 1.003 |

## What this shows

- The pipeline runs end to end: form-finding, S8R deck, CalculiX, parsing.
- Both periods are far below Tg = 0.35 s, so both shells sit on the spectrum plateau (S5 holds for this case).
- Corner support is the hard case. The 168 designs will be decided by corner-supported shells: λ = 11.8 at 80 mm, against the λ ≥ 5 limit. [J]
- Reaction check: CalculiX's support reaction leaves out self-weight lumped straight onto a fixed node. With 80 fixed edge nodes the sum is 7 % short; with 4 fixed corners it matches the weight to 0.3 %. So equilibrium is checked on corner-supported shells (`tests/test_fe.py`).

## Decision made today (Claude, under delegation)

- **D3-1** [J]: with equal force densities the free edges of a corner-supported net pulled in by 2.4 m on a 10 m span, leaving 38 % of the plan. Corner forms now use a boundary force density set so the mid-edge inset is 0.10 x span (factor 18.5). Recorded as a pre-registration amendment.

## Open

- ν and density from a ShellBench tag (not supplied here).
- Cross-check `fe.py` against ShellBench `floor-r2` when it is tagged (due 2 Nov).
- Mesh check (21 vs 41 nodes per side) before the design runs.
