# Handoff between Claude in the app and Claude Code in VS Code

Newest entry first. Each Claude reads this at the start of a session and adds an entry at the end (see "Sync with cloud Claude" in CLAUDE.md).

## 30 Oct 2026, Claude Code in VS Code (Day 2 sync)

**Done:** pulled main (Day 1 and Day 2 work from the app); ShellBench-pin is at `v0.0.1`, matching `SHELLBENCH_TAG`; `pip install -e . --no-deps`; pytest 25 passed. The Day 2 handoff names no scripts to run. `results/` holds only `README.md`, unchanged.

**Decisions by the author today:** none new in this session; the standing delegation still applies.

**Open:** nothing new. Open items from the app entry above still stand. A local blank-line edit to `LOG.md` is kept in `git stash` (not applied; no content).

**Next:** 31 Oct, move the pin when floor-r1 is tagged; S1b cross-check.
## 30 Oct 2026, Claude in the app (Day 2, pre-registration approved)

**Done:** 3D force density solver (`formfind.py`), strategies and envelope thickness (`strategies.py`), tests 11 → 25 passed. `docs/preregistration.md` approved, with decisions P1 (strategy 2 = midrange of the four sheared thrust surfaces), P2 (own 3D solver; floor-r1 as the 2D cross-check), P3 (GB/T 51366 plus a ±25 % band; no ICE). Thresholds: λ_LBA ≥ 5 (3, 8), L/300 (GB 50010 Table 3.4.3, p. 11 [check]), t_min 50 mm, 5 mm steps. `docs/data_contract.md` amended.

**Decisions by the author today:** standing delegation: "do not ask me ever. you do it based on the best that you think". Every decision above was made by Claude under it and is marked as such.

**Open (author, whenever convenient; nothing waits on them):** confirm the [check] items in your copies (GB 50010 Table 3.4.3; IASS 1979 / Dulácska & Kollár 1995 for buckling); the Michiels full texts (S4 falls back to a closed form on 4 Nov).

**Next:** 31 Oct, move the pin to v0.1/floor-r1 when tagged; S1b against floor-r1; CalculiX deck for one shell.

## 29 Oct 2026, Claude in the app (Day 1, author away)

**Done:** `notes/michiels2017.md` (from abstracts only; [check] marks what needs the full text); `src/shellform/checks.py` with `equilibrium_error` (S2) and `rotation_error` (S3), solver-independent so they run on floor-r1 unchanged; `src/shellform/design_space.py` (168 cases, `spans=(10.0,)` gives the 84-case stop-loss space, results columns include `shellbench_tag`); tests 2 → 11 passed. The tests use a small test-only force density solver; it is not ShellForm's form-finder.

**Finding F1:** with fixed nodal loads, a uniform lateral load only shears the gravity form, x = x_g - Sa z_g. Added as an open decision in `docs/preregistration.md` section 2.

**Decisions by the author today:** "finish everything for today yourself". No research decision was taken for the author.

**Open (author):**
- ShellBench Day 12: six carbon factor lines, and "f_c and minimum confirmed" (GB 50010 Table 4.1.4-1 printed p. 19; Table 11.3.6-1 printed p. 168).
- Choose the reversal rule (a, b or c) and approve the pre-registration (30 Oct).
- ResearchGate request for the Michiels full texts (S4 depends on them).

**Next:** Day 2 (30 Oct), pre-registration approval.

## 28 Oct 2026, Claude in the app (Day 0 scaffold)

**Done:** repository structure; `src/shellform/pin.py` pins ShellBench `v0.0.1` (the only tag today); `docs/data_contract.md` copied from the project file `10_ShellForm_Reference_Data.md`; draft `docs/preregistration.md` from contract sections 3-4; `explorer/index.html` skeleton (three.js, dummy data, labelled as such); smoke tests.

**Decisions by the author today:** start ShellForm on 29 Oct; build ends 13 Nov; check window 14-17 Nov.

**Open (author):**
- Approve or change `docs/preregistration.md`. It must be committed before any run.
- Get the four Michiels & Adriaenssens papers (test S4 depends on them).
- Send ShellBench "What ShellForm needs" (contract section 6) by Mon 2 Nov.
- Read GB 50011 Table 5.1.4-1 design and rare alpha_max, and an EN 1998-1 example site, before they become plot markers [?].

**Next:** Day 1 (29 Oct), Michiels 2017 reading notes and pre-registration approval.
