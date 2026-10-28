# ShellForm pre-registration

**Status: DRAFT, 28 Oct 2026. Not approved.** The author approves or changes this file, then it is committed before any form-finding run. After approval, changes only by a dated amendment at the end that says why.

Sources: `docs/data_contract.md` sections 3-4. Values from ShellBench are named by module, never copied. Items marked [?] need the author's reading of a source; items marked [J] are Claude's proposal for the author to accept or change.

## 1. Research question

How much embodied carbon does seismic resilience cost in a form-found concrete shell, and does seismic-aware form-finding deliver it more cheaply than thickening a gravity-only shape?

## 2. Strategies

1. **Gravity-only:** form from ShellBench's force density method (`floor-r1`) under gravity; then size the thickness (and tension reinforcement) to pass all checks at each Sa level.
2. **Seismic-aware:** form from the same method with lateral load cases added after Michiels & Adriaenssens (ShellForm's own code); then size it to pass the same checks.

The only difference between the strategies is the form. Checks, materials, sizing rule and carbon factors are identical.

## 3. Design space (168 sized designs)

| Variable | Levels |
|---|---|
| Plan | Square |
| Span | 10 m, 20 m |
| Supports | 4 corner supports; continuous edge supports |
| Rise-to-span | 0.10, 0.15 (baseline), 0.20 |
| Strategy | gravity-only; seismic-aware |
| Plateau spectral acceleration Sa | 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 g |

Site markers on plots: Panzhihua frequent earthquake (ShellBench `seismic.alpha_max_frequent(7, 0.10)`). Panzhihua design and rare levels and one EN 1998-1 example site are added only after the author reads them in GB 50011 Table 5.1.4-1 and EN 1998-1 [?].

## 4. Loads and materials

All from ShellBench at the pinned tag: site and Tg (decision B5), concrete and steel design values (`notes/gb50010_design_values.md`), seismic combination (flag D21), roof dead and live loads (spec L2, L11; superimposed dead load to be confirmed against L2 [?]). How the lateral load is applied in form-finding (direction, distribution over the mass, sign cases) is written here after the Michiels 2017 reading, before any run [?].

## 5. Checks (pass/fail for sizing)

| Check | Rule | Threshold |
|---|---|---|
| Concrete compression | stress <= fc | ShellBench value |
| Tension zones | As = T / fy, at least the minimum ratio | ShellBench value |
| Linear buckling | factor >= lambda_min | From literature [?]; sensitivity at two other values |
| Deflection | <= limit | With a source [?] |
| Minimum thickness | >= t_min | Constructible value with a source [?] |

Sizing rule: the minimum thickness, in steps of [?] mm [J: 5 mm], that passes every check in every load combination.

## 6. Carbon

A1-A3 of concrete and reinforcement from ShellBench `data/carbon_factors.csv`, reported under both the GB/T 51366 and the ICE factor sets.

## 7. Decision rules (written before any result)

- **Cost of resilience:** for each form family, carbon at Sa divided by carbon at Sa = 0, for each strategy.
- **Which strategy is cheaper:** at each (span, supports, rise, Sa), the strategy with lower carbon. A difference smaller than [J: 5 %] is reported as "no meaningful difference".
- **Headline claim** ("seismic-aware form-finding is cheaper") is made only if it holds under **both** factor sets and at the baseline rise of 0.15 for both supports. Otherwise the result is reported as conditional, with the cases where it holds.
- **Robustness:** the headline is re-checked at the two other buckling thresholds and one finer mesh. A conclusion that flips is reported as sensitive.
- A design that cannot pass at any thickness up to [J: span/50] is reported as infeasible, not dropped.

## 8. Validation (tests S1-S5)

| Test | Proves | Pass |
|---|---|---|
| S1 Zero lateral load | Seismic-aware form with Sa = 0 equals the `floor-r1` gravity form | Machine precision |
| S2 Nodal equilibrium | Each free node in equilibrium under gravity + lateral loads | Residual < 1e-9 of the load |
| S3 Rotation | Rotating all loads and supports by one angle rotates the form by that angle | Error < 1e-9 |
| S4 Published case | Reproduces one Michiels & Adriaenssens example from its stated inputs | Tolerance stated here before running [?] |
| S5 Plateau | First-mode period of every sized design below Tg (`floor-r2` modal) | Any failure reported with its real spectral value |

ShellBench's own tags cover the gravity form-finder (1 %) and the shell wrapper (2 %); ShellForm cites them.

## 9. Freeze

Code and analysis frozen on 10 Nov 2026 (commit hash recorded here). Results for the paper come from one run after the freeze.

## Amendments

None.
