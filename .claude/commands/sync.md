---
description: Daily sync for ShellForm: pull, test, hand off. Run once at the end of each day.
---

Do the daily sync for ShellForm. Do every step yourself without asking me, then report.

Use the conda env `shellform` (never `research`): `C:\Users\ASUS\miniconda3\Scripts\conda.exe run -n shellform <command>`.

1. `git checkout main` and `git pull origin main`. Read the newest entry in `docs/handoff.md` and the newest day in `LOG.md`.
2. In `C:\Users\ASUS\ShellBench-pin`, check that the checked-out tag matches `SHELLBENCH_TAG` in `src/shellform/pin.py`. If it does not, report it and stop.
3. `pip install -e . --no-deps`, then `pytest`. Note the pass count.
4. Run every script the newest handoff entry names. `git status`: every file in `results/` must be unchanged unless today's task changed it on purpose.
5. Add a dated entry at the top of `docs/handoff.md` ("Claude Code in VS Code").
6. Commit as me (Syed Nafiz Reja Hasib <syednafiz2811@gmail.com>) on a branch `dayNN-sync`, push, open a PR and merge it if the tests passed. No Claude attribution anywhere.
7. Report in at most five lines: last handoff, pytest result, results identical or not, PR number, anything that needs me.
