# ShellForm Data Contract — what comes from ShellBench, what ShellForm owns

**Prepared:** 28 October 2026, after reading the ShellBench repo (`docs/baseline_spec.md`, `docs/schedule.md`, `docs/handoff.md`, `notes/`, `src/shellbench/`, `LOG.md`).
**Replaces** the earlier version of this file. The earlier version gave values from the thesis and from memory. ShellBench has since checked and corrected many of them, and some (the carbon factors) are yours to enter, not Claude's.

## 1. The rule: best data wins, and there is one home for it

| Priority | Source | Examples |
|---|---|---|
| 1 | **ShellBench tagged releases and your recorded decisions** | `docs/baseline_spec.md` decisions B1–B16; `notes/gb50010_design_values.md`; `notes/gb50011_base_shear_primer.md`; `data/carbon_factors.csv`; the validated floor modules floor-r1, floor-r2, floor-r3 and v0.3 |
| 2 | **Code values you have confirmed in your own copy** | Marked "confirmed" in ShellBench notes |
| 3 | **ShellForm-only choices, pre-registered in ShellForm** | Sa sweep, plan geometry, buckling threshold, explorer |

ShellForm **never copies a ShellBench value into its own files**. It imports ShellBench (pinned to a tag) or reads ShellBench's data files. If a value changes in ShellBench, ShellForm picks it up and the change is visible in both logs. Every ShellForm result names the ShellBench tag it used.

The same rules as ShellBench's `CLAUDE.md` apply: Claude never supplies carbon factors or code values; you read them from the source. Unconfirmed values stay marked [?].

---

## 2. What ShellForm takes from ShellBench (in ShellBench's own hand-over order)

| ShellBench tag (latest date) | What it gives ShellForm | Already validated by | ShellForm uses it for |
|---|---|---|---|
| `data/carbon_factors.csv` (you, Thu 29 Oct) | C30/C35/C40 and HRB400 factors, GB/T 51366 and ICE | Your reading of the sources | All carbon numbers, both factor sets |
| **v0.1** (Sat 31 Oct) | Anchor site and materials as decided (B1–B16), code values in `notes/` | Anchor report, Days 5–13 | Site, materials, load factors |
| **floor-r1** (Sat 31 Oct) | Force density form-finding code | Parabola and thrust tests within 1% | The gravity-only form-finder ShellForm extends |
| **floor-r2** (Mon 2 Nov) | CalculiX shell analysis wrapper | Scordelis-Lo roof and pinched hemisphere within 2% | All shell analysis (static, modal, buckling) |
| **floor-r3** (Tue 3 Nov) | One sized panel: thickness, tie, buckling factor, quantities | Tie force within 10% of the closed form | The sizing and check functions |
| **v0.3** (Thu 5 Nov) | Floor library (60+ cases) and topping rule | 5 spot checks | Context only: comparing roof shells with floor vaults in the Discussion |

**ShellForm does not need the building family dataset (11 Nov DOI) or any parquet columns.** Tell ShellBench this by Mon 2 Nov (text in section 6). That takes one risk out of ShellBench's 4 Nov format freeze.

### Values already settled in ShellBench that ShellForm inherits
- **Site:** Panzhihua, intensity 7, 0.10 g, Group 1, **site class II, Tg = 0.35 s** (decision B5, your reading of GB 50011 Table 5.1.4-2).
- **Frequent-earthquake αmax = 0.08** (confirmed by you in Table 5.1.4-1, 25 Oct). The design-earthquake and rare-earthquake αmax are **not yet confirmed** in ShellBench: read them in Table 5.1.4-1 before they are used as plot markers [?].
- **Spectrum:** `shellbench.seismic.alpha_spectrum()`, already coded with its clauses. ShellForm calls it; it does not write its own.
- **Concrete C40:** fc 19.1, ft 1.71, Ec 3.25 × 10⁴ N/mm², ν 0.2; **HRB400:** fy 360, Es 2.0 × 10⁵ N/mm² (GB 50010, checked against the Chinese 2015 edition, `notes/gb50010_design_values.md`).
- **Minimum steel ratio (non-seismic flexural member):** max(0.20%, 45 ft/fy) = 0.214% (Table 8.5.1).
- **Seismic combination for new designs:** 1.3 G_E + 1.4 E_h (GB 55002-2021 cl. 4.3.2, flag D21). Thesis factors 1.2/1.3 stay for thesis validation only.
- **Cover:** your reading of GB 50010 Table 8.2.1, environment class I, gives 15 mm minimum for slabs (decision B14). Check whether shells share that row in your copy [?].
- **Roof loads:** non-accessible roof live load 0.5 kN/m² (spec L11); roof finishes from the thesis roof build-up (spec L2: total 4.224 kN/m² including the 120 mm slab at 3.00). Superimposed roof dead load is therefore about 1.0 kN/m² [J]. Confirm against spec L2 before use.

---

## 3. What ShellForm owns (pre-register these before any run)

| Item | ShellForm choice | Status |
|---|---|---|
| Research question | How much embodied carbon does seismic resilience cost in a form-found concrete shell, and does seismic-aware form-finding deliver it more cheaply than thickening a gravity-only shape? | Fixed |
| Plan and supports | Square plan; 4 corner supports and continuous edge supports | Fixed |
| Spans | 10 m and 20 m | Fixed |
| Rise-to-span | 0.10, 0.15 (baseline), 0.20 | Fixed |
| Strategies | (1) gravity-only form + size to pass; (2) seismic-aware form (lateral load cases added to ShellBench's force density method, after Michiels & Adriaenssens) + size to pass | Fixed |
| Seismic axis | Plateau spectral acceleration **Sa = 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 g**. Shells have short periods, so they sit on every code's plateau. Check this for every design and report any exception [J] | Fixed |
| Site markers on plots | Panzhihua frequent 0.08 g (confirmed). Panzhihua design and rare levels, and a Eurocode 8 example site, **only after you read the values in GB 50011 Table 5.1.4-1 and EN 1998-1** [?] | Pending your reading |
| Checks | Concrete stress ≤ fc; tension zones reinforced (As = T/fy, ≥ minimum ratio); linear buckling factor ≥ a threshold you justify from literature (sensitivity at two other values); deflection limit with a source; minimum constructible thickness with a source | Thresholds pending literature |
| Carbon | A1–A3 from `data/carbon_factors.csv`; results with both GB/T 51366 and ICE sets; conclusion must hold under both | Fixed |
| Runs | 2 spans × 2 supports × 3 rises × 2 strategies × 7 Sa levels = **168 sized designs** | Fixed |

---

## 4. ShellForm's own validation (only what ShellBench doesn't already cover)

ShellBench validates the force density method under gravity (1%) and the CalculiX shell wrapper (Scordelis-Lo and pinched hemisphere, 2%). ShellForm cites those tags and adds tests for the part that is new:

| Test | What it proves | Pass |
|---|---|---|
| **S1. Zero lateral load** | Seismic-aware form-finding with Sa = 0 returns exactly the floor-r1 gravity form | Identical to machine precision |
| **S2. Nodal equilibrium** | Every free node is in equilibrium under the combined gravity + lateral load set | Residual < 1 × 10⁻⁹ of the load |
| **S3. Rotation test** | The force density equations are linear, so rotating every load and every support by the same angle must rotate the form by that angle exactly. This checks the lateral-load code independently | Error < 1 × 10⁻⁹ |
| **S4. Published case** | Reproduce one published Michiels & Adriaenssens example (arch or shell form under lateral load) from the paper's stated inputs | Within the tolerance you can read from their figures; state it before running [J] |
| **S5. Plateau check** | First-mode period of every sized design below Tg, from the floor-r2 modal analysis | Report any design that fails, with its real spectral value |

Get the Michiels papers this week (ResearchGate request to the authors, or your library). S4 depends on them.

---

## 5. Dates (aligned with ShellBench's schedule)

| Date | ShellForm work | Depends on |
|---|---|---|
| 29–30 Oct | Repo set up; read Michiels 2017 (C&S) and 2018; write `docs/preregistration.md` (sections 3–4 of this file, with decision rules); explorer skeleton (three.js, dummy data) | Nothing from ShellBench |
| 31 Oct–1 Nov | Import floor-r1; add lateral load cases; tests S1–S3 | floor-r1 |
| 2–3 Nov | Square-plan shell generator; analysis through floor-r2 (static, modal, buckling) | floor-r2 |
| 4–5 Nov | Sizing loop through floor-r3 checks; test S4. **Send ShellBench the "no family columns needed" note by 2 Nov** | floor-r3 |
| 6–9 Nov | Run 168 designs; carbon with both factor sets; sensitivity; S5; figures | carbon_factors.csv, v0.3 |
| 10 Nov | **ShellForm code and analysis frozen** (commit), same protocol as ShellBench's surrogate | — |
| 11–13 Nov | Final figures, explorer with real results, README, ShellForm v0.1 + Zenodo DOI; you draft Methods and Results | — |
| 14–17 Nov | Check window, shared with ShellBench: you check every number; Claude fixes | — |
| After 17 Nov | You write Discussion, Introduction, Abstract; preprint; submit to Computers & Structures (target: before the European deadlines in January) | — |

**Shared allowance:** ShellBench and ShellForm use one Claude Pro allowance. Until 11 Nov, ShellBench GATE days come first, as ShellBench's schedule already says. Keep ShellForm chats short. Do the coding in Claude Code with the repo open, and use the app only for planning and review.

---

## 6. Text to send ShellBench by Mon 2 Nov ("What ShellForm needs")

Paste into the ShellBench Project chat, or into `docs/handoff.md` through Claude Code:

> **What ShellForm needs from ShellBench (author, [date]):**
> 1. Floor-level code only: floor-r1 (force density), floor-r2 (CalculiX shell wrapper), floor-r3 (sizing, tie, buckling and quantity functions), with their public function signatures kept stable after each tag. ShellForm pins to the tags.
> 2. `data/carbon_factors.csv` and the material and code values in `notes/`, read in place, not copied.
> 3. `shellbench.seismic.alpha_spectrum()` and the site values from `docs/baseline_spec.md` (B5).
> 4. **No columns from the building family dataset.** The 4 Nov format freeze does not need to include anything for ShellForm.
> 5. Request: export the force density solver and the CalculiX wrapper as public functions with docstrings, so ShellForm can import them without reaching into private code.

---

## 7. Literature ShellForm builds on (DOIs checked)

- Michiels & Adriaenssens 2017, Computers & Structures: 10.1016/j.compstruc.2017.10.001
- Michiels & Adriaenssens 2017, Engineering Structures: 10.1016/j.engstruct.2017.10.043
- Michiels, Adriaenssens & DeJong 2018, Engineering Structures: 10.1016/j.engstruct.2018.12.043
- Michiels, Adriaenssens & Jorquera-Lucerga 2017, J. IASS: 10.20898/j.iass.2017.194.892
- Tomasello, Adriaenssens & Gabriele 2019, Engineering Structures: 10.1016/j.engstruct.2019.109521
- Pérez Vega et al. 2026, Research on Engineering Structures and Materials: 10.17515/resm2026-1812st0804rs
- Oval et al. 2023, Structures: 10.1016/j.istruc.2023.01.063
- Mesnil et al. 2025, Automation in Construction: 10.1016/j.autcon.2025.106076
