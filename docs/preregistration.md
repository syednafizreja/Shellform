# ShellForm pre-registration

**Status: APPROVED 30 Oct 2026, before any form-finding run of the design space.** It was approved by Claude under the author's standing delegation of 30 Oct 2026 ("do not ask me ever. you do it based on the best that you think"). The author may reverse any choice by a dated amendment. After approval, changes are made only by a dated amendment at the end that says why.

Markers: [J] = Claude's judgement. [check] = read by Claude, still to be confirmed by the author in the source. [?] = still open, with the rule that closes it. Values from ShellBench are imported from the pinned tag (`src/shellform/pin.py`), never copied.

## 1. Research question

How much embodied carbon does seismic resilience cost in a form-found concrete shell, and does seismic-aware form-finding deliver it more cheaply than thickening a gravity-only shape?

## 2. Strategies

Both strategies use ShellForm's own 3D force density solver (`src/shellform/formfind.py`; section 8, S1b). ShellBench `floor-r1` form-finds a 2D vault curve, not a doubly curved shell, so it is the 2D cross-check, not the solver (decision P2 below).

**Thrust surfaces.** For a force density pattern q, the gravity form G has heights z_G. Under gravity plus a horizontal acceleration Sa in direction d (one of +x, -x, +y, -y), the admissible thrust surfaces of the same pattern scaled by 1/λ are T(d, λ): heights λ z_G, moved horizontally by -Sa λ z_G d (finding F1, `notes/michiels2017.md`). λ > 0 is free, because the horizontal thrust of a funicular is statically free.

**Envelope thickness.** For a mid-surface M, t_env(M, Sa) is twice the largest gap, measured normal to M (vertical gap times the cosine of M's slope), between M and the nearest admissible thrust surface. For each direction d, λ is chosen to minimise that gap, and the worst of the four directions governs. This is the lower-bound (safe theorem) requirement used by Michiels & Adriaenssens, applied to the four shaking directions [J].

1. **Gravity-only (strategy 1):** M = G, the gravity form of uniform q (corner supports: boundary edges at 4 q [J]). Size it at each Sa.
2. **Seismic-aware (strategy 2):** M = the midrange height, at each plan point, of the four thrust surfaces T(±x, λ*), T(±y, λ*) at the design Sa, that is halfway between the highest and the lowest of them, with λ* set so that M has the target rise (`src/shellform/strategies.py`). This is a form-found surface that includes the lateral load cases. It plays the role of the middle surface between Michiels' double layers [J; check against the IASS 2017 full text]. Size it at the same Sa.

The strategies differ only in the mid-surface. Checks, materials, the sizing rule and the carbon factors are identical. At Sa = 0, M = G for both (S1).

**Decision P1 (30 Oct, Claude):** a single sheared form (draft option a) suits shaking in one direction only. Averaging +x and -x shears without rescaling gives back G exactly. So strategy 2 is defined by the four-direction thrust-surface mean above (draft option c, refined). It is the simplest definition in which the lateral load changes the form [J].

## 3. Design space (168 sized designs)

| Variable | Levels |
|---|---|
| Plan | Square |
| Span L | 10 m, 20 m |
| Supports | 4 corner supports; continuous edge supports |
| Rise-to-span | 0.10, 0.15 (baseline), 0.20 |
| Strategy | gravity-only; seismic-aware |
| Plateau spectral acceleration Sa | 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 g |

Coded in `src/shellform/design_space.py`. Network for form-finding: 41 x 41 nodes [J]; mesh sensitivity at 61 x 61 (section 7).

Site markers on plots: the Panzhihua frequent earthquake, from ShellBench `seismic.alpha_max_frequent(7, 0.10)` times η2 = 1.0. The design and rare levels and one EN 1998-1 site are added only once they are read in GB 50011 Table 5.1.4-1 and EN 1998-1 [check]. Markers do not change any result.

## 4. Loads and materials

- **Form-finding load:** uniform load per unit plan area, with the lateral load as Sa times the same nodal weights (Michiels & Adriaenssens, C&S 2018 highlights: horizontal acceleration as a first-order approximation of seismic action). The form does not depend on the load magnitude once the rise is fixed.
- **Analysis loads:** shell self-weight at the ShellBench unit weight for reinforced concrete (spec X7); roof superimposed dead load and non-accessible roof live load from ShellBench (spec L2, L11); G_E = dead load only, because GB 50011 Table 5.1.3 takes no roof live load into the representative gravity load, as ShellBench's anchor does [check].
- **Seismic action:** equivalent static horizontal load Sa x G_E in each of +x, -x, +y, -y, separately. Shells are short-period, so they sit on the plateau (checked by S5). Vertical seismic action is not included (as in ShellBench).
- **Combinations:** ShellBench `combinations.CODE_SEISMIC_COMBINATIONS` (1.3 G_E + 1.4 E_h, GB 55002-2021, flag D21) and its gravity combinations.
- **Materials:** C40 and HRB400 design values imported from ShellBench `checks` (f_c, f_t, f_y) and E_c from the ShellBench spec.

## 5. Checks (pass/fail for sizing)

| Check | Rule | Threshold and source |
|---|---|---|
| Concrete compression | principal compressive stress <= f_c | ShellBench f_c |
| Tension | A_s = T / f_y, at least ρ_min | ρ_min = max(0.15 %, 45 f_t/f_y) for slabs, as ShellBench's floor concept [J: slab rule applied to shells] |
| Linear buckling | load factor λ_LBA >= 5 | [J], from the reduction-factor approach of the IASS Recommendations for reinforced concrete shells (1979) and Dulácska & Kollár (1995), which reduce the linear buckling load for imperfections, creep and cracking, then apply a safety factor of 1.5 to 3.0 [check]. Sensitivity at 3 and 8 |
| Deflection | <= L/300 under the quasi-permanent combination | GB 50010-2010 (2015) Table 3.4.3, roof members with l0 > 9 m, printed p. 11 [check] |
| Minimum thickness | t >= 50 mm | Cover to mesh on both faces, as in ShellBench's floor concept section 4 [J] |

**t_env is reported, not checked.** It is the thickness an unreinforced shell would need to keep a compression-only path (Michiels' masonry criterion). The shells here are reinforced, so tension and bending are carried by the checks above; t_env explains the results but does not size them [J].

**Sizing rule:** the smallest thickness, in 5 mm steps from 50 mm, that passes every check in every combination. Uniform thickness per shell [J]. A design that fails at every thickness up to L/50 is reported as infeasible, not dropped.

## 6. Carbon

A1-A3 of concrete and reinforcement, from ShellBench `data/carbon_factors.csv` (GB/T 51366-2019 Table D.0.1; C40 = 340 kgCO₂e/m³ is ShellBench's interpolation [J]).

**Decision P3 (30 Oct, Claude):** ICE is not used. ShellBench's D29 found that its licence forbids distributing its values, and ShellForm's repository is public. Instead, a **factor band**: every result is recomputed with the concrete and steel factors each at ±25 %, independently, which gives four corners [J]. Carbon is reported per m² of plan area.

## 7. Decision rules (written before any result)

- **Cost of resilience:** for each (span, supports, rise, strategy), carbon at Sa divided by carbon at Sa = 0.
- **Which strategy is cheaper:** at each (span, supports, rise, Sa), the strategy with the lower carbon. A difference smaller than 5 % is reported as "no meaningful difference" [J].
- **Headline claim** ("seismic-aware form-finding is cheaper"): made only if it holds at all four corners of the factor band, and at rise-to-span 0.15 for both supports, at every Sa >= 0.2 g. Otherwise the result is reported as conditional, naming the cases where it holds.
- **Robustness:** the headline is re-checked at λ_LBA = 3 and 8, and with a 61 x 61 network. A conclusion that flips is reported as sensitive.
- No result is dropped. Infeasible designs are reported as infeasible.

## 8. Validation (tests S1-S5)

| Test | Proves | Pass |
|---|---|---|
| S1 Zero lateral load | Strategy 2 with Sa = 0 equals the gravity form | Machine precision |
| S1b 2D limit | ShellForm's solver gives the exact nodal parabola for a chain (done), the membrane centre value 0.0737 p L²/T for an edge-supported net (done, within 1 %) [check], and ShellBench `floor-r1`'s vault curve once tagged | Exact; 1 %; 1 % |
| S2 Nodal equilibrium | Every free node in equilibrium under gravity + lateral loads | Residual < 1e-9 of the load |
| S3 Rotation | Rotating all loads and supports rotates the form by the same angle | Error < 1e-9 |
| S4 Published case | One Michiels & Adriaenssens arch (C&S 2018: rise-to-span 1/4, 0.3 g) from its stated inputs | Tolerance fixed here once the full text is read [?]. If the full text is not available by 4 Nov, S4 is replaced by the closed-form lean of a parabolic arch under uniform horizontal acceleration, and the paper says so |
| S5 Plateau | First-mode period of every sized design below Tg = 0.35 s (ShellBench B5), from a CalculiX modal run | Any failure reported with its real spectral value |

The shell analysis uses ShellBench's CalculiX wrapper (`floor-r2`, validated on the Scordelis-Lo roof and the pinched hemisphere within 2 %), which ShellForm cites.

## 9. Freeze

Code and analysis are frozen on 10 Nov 2026 (commit hash recorded here). Results for the paper come from one run after the freeze.

## Amendments

**30 Oct 2026 (Claude, under delegation), made before any design-space run.** Compared with the 28 Oct draft: P1 (strategy 2 defined as a four-direction thrust-surface mean, plus the envelope check), P2 (ShellForm's own 3D solver, with floor-r1 as the 2D cross-check), P3 (ICE replaced by a ±25 % factor band). Thresholds set: λ_LBA 5 (3, 8), L/300, 50 mm, 5 mm steps, L/50 infeasible limit, 5 % band.

**30 Oct 2026, later the same day (Claude, under delegation), still before any design-space run.** While writing the unit tests on 10 m test nets (not design cases), two definitions were corrected: (1) strategy 2 uses the midrange, not the mean, of the four thrust surfaces, because the midrange is the centre of the band that must hold all four; (2) t_env is measured normal to M and is reported, not used as a pass/fail check, because it is a criterion for unreinforced shells. In those tests, the strategy 2 surface changed t_env by less than 4 % (`notes/michiels2017.md`, F2). This was seen before the change. No definition was tuned to make strategy 2 look better, and the 5 % decision rule stands.

**31 Oct 2026 (Claude, under delegation), before any design-space run.** Two additions from the first CalculiX run on one shell (`notes/day03_one_shell.md`): (1) **D3-1** [J]: corner-supported forms use a boundary force density set by bisection so the free edge insets by 0.10 × span at mid-edge (factor 18.5, the same for all spans and rises, because plan equilibrium does not depend on q scaling). With equal force densities the free edges pulled in by 0.24 × span and the shell kept only 38 % of its plan area, which is not a buildable roof. The 0.10 value is a judgement, and it is reported with the results. (2) Section 8 names ShellBench's `floor-r2` CalculiX wrapper. It is not tagged yet, so ShellForm writes its own S8R deck (`src/shellform/fe.py`). When `floor-r2` is tagged, both are run on the same shell and the difference is reported; ShellBench's wrapper is used for the results if they differ by more than 2 %. Neither change was chosen to favour either strategy: both strategies use the same supports and the same rule.
