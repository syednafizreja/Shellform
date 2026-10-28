# CLAUDE.md

Rules for Claude when working in this repository. They follow ShellBench's CLAUDE.md, plus the ShellForm data rule.

## Rules

1. Never invent references, numbers, code clauses, results or DOIs. If unsure, say "I don't know" and tell me how to check.
2. **ShellForm never copies or hard-codes a ShellBench value.** Import `shellbench` (pinned in `src/shellform/pin.py`) or read ShellBench's data files in place. Never supply carbon factors or code values; I read them from the source. Unconfirmed values stay marked [?]. The data contract is `docs/data_contract.md`.
3. When a number comes from a code, give the clause, and tell me to confirm it in my copy of the code. When it comes from a paper, give the page, table or figure.
4. When you write code, give complete files with the file path at the top, then explain them section by section in plain English. SI units.
5. When I paste an error, first explain the cause in one or two sentences, then give the complete corrected file.
6. Keep me on today's task. If I drift, remind me of today's Done-when line.
7. Never use or ask for data from my former employer.
8. Writing style: plain British English, short sentences, no hype words ("novel", "first", "groundbreaking"). ShellForm extends Michiels & Adriaenssens; never call it "the first seismic form-finding". Mark your own judgement with [J].
9. Nothing in `docs/preregistration.md` changes after it is approved without a dated amendment that says why.

## Code standards

SI units everywhere; every function has a docstring; no hidden constants; every number in a result traces to ShellBench (tag named), a code clause, a paper or this repo's code. Every file in `results/` names the ShellBench tag it used.

## Environment

- Windows 11, PowerShell, conda environment `research` (Python 3.12), shared with ShellBench. Run commands with `C:\Users\ASUS\miniconda3\Scripts\conda.exe run -n research <command>`.
- ShellBench is installed in editable mode from a separate read-only clone, `C:\Users\ASUS\ShellBench-pin`, checked out at the tag in `src/shellform/pin.py`. Never edit files in that clone; ShellBench work happens in `C:\Users\ASUS\ShellBench`.

## Sync with cloud Claude

Two Claudes work on this project: Claude in the Claude app (cloud, ShellForm project threads) and Claude Code in VS Code (this laptop). The repo carries the handover.

- **At session start:** `git pull origin main`, then read `docs/handoff.md` (newest entry first) and the latest entry in `LOG.md`. Tell me in one line what the last handoff said.
- **At session end:** add a dated entry at the top of `docs/handoff.md`: what you did, decisions I made, what is open. Commit and push it with the work.
- **ShellBench comes first** until 11 Nov: its GATE days are never displaced by ShellForm work.
- **No Claude attribution, anywhere:** no `Co-Authored-By: Claude` trailers, no `Claude-Session:` links, no "Generated with Claude Code" lines in commits, PRs, issues or comments. Commit as me (Syed Nafiz Reja Hasib <syednafiz2811@gmail.com>). No branch names starting `claude/`.
