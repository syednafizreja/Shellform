# ShellForm LOG

## Day 0 — 28 Oct 2026
- Done: repository structure, pin to ShellBench v0.0.1, data contract copied to docs/, draft pre-registration, explorer skeleton with dummy data
- Result: —
- Problem: ShellBench floor-r1/r2/r3 not tagged yet (due 31 Oct, 2 Nov, 3 Nov)
- Lesson: —
- Tomorrow: Day 1, read Michiels & Adriaenssens 2017 (C&S) and approve docs/preregistration.md

## Day 1 — 29 Oct 2026
- Done (Claude, author away): reading notes `notes/michiels2017.md` from the open abstracts of the C&S 2018 and J. IASS 2017 papers (full texts not yet read); `src/shellform/checks.py` (S2 equilibrium error, S3 rotation error) and `src/shellform/design_space.py` (168 cases, results columns); 9 new tests
- Result: pytest 11 passed. Finding F1: a uniform lateral load in force density only shears the gravity form (x = x_g - Sa z_g), confirmed to 1e-12
- Problem: full texts of the Michiels papers not available yet; ShellBench Day 12 still waits on the author's carbon factors and the f_c / minimum confirmation
- Lesson: "add lateral loads" alone gives a one-directional form; the load-reversal rule must be chosen before the pre-registration is approved
- Tomorrow: Day 2, choose the reversal rule (a/b/c), fill the remaining [?] and approve docs/preregistration.md
