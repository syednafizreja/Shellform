---
description: Do today's ShellForm task list end to end without asking me, then report. Pass the list as arguments, or leave it empty to use the handoff.
argument-hint: [today's task list]
---

Do today's tasks for ShellForm. Do every step yourself. Do not ask me anything unless the step truly cannot be done by you, even with full permission and access (for example, it needs my login to a website, or a rule in CLAUDE.md says only I may do it). Collect those items and report them at the end. Do not stop at them.

All credit is mine. Commit as me (Syed Nafiz Reja Hasib <syednafiz2811@gmail.com>). No Claude attribution in any file, commit, PR, issue or comment.

Use the conda env `shellform` (never `research`): `C:\Users\ASUS\miniconda3\Scripts\conda.exe run -n shellform <command>`.

## 1. Get the list

- Today's list is: $ARGUMENTS
- If that is empty, use the "Next" line of the newest entry in `docs/handoff.md`, its "Open" items, and the "Tomorrow" line of the newest day in `LOG.md`.
- Order the list so ShellBench GATE items come first (ShellBench comes first until 11 Nov).

## 2. Do each task

Apply CLAUDE.md to every task. In particular:

- **ShellBench tasks** happen in `C:\Users\ASUS\ShellBench`, following that repo's own CLAUDE.md. Never edit `C:\Users\ASUS\ShellBench-pin`.
- **Carbon factors and code values** (CLAUDE.md rule 2): never write a value yourself. Find the source file, the table or clause, and the exact lines, and prepare everything around them. I enter or confirm the values. Put each item in the report as "needs you" with the source and the location.
- **Papers**: find them yourself first: DOI lookup, publisher page, open-access copies, repositories, and the research search tools. Save any PDF you get to `data/papers/` (ignored by git if it is not open access). Only report a paper as "needs you" if no legal copy can be reached, and name the action (for example "request on ResearchGate: <link>").
- **Reading notes** (`notes/*.md`): fill in every heading from the paper itself. Give the page, figure, table or equation number for each fact. Quote numbers exactly as printed. Anything you cannot read in the paper stays `[?]`. Mark your own judgement with [J]. Never fill a note from memory.
- **"/sync" in the list**: run the `sync` command last, after every other task.

## 3. Check

- Run `pytest`. If anything you changed breaks it, fix it before you finish.
- `git status`: nothing in `results/` changes unless a task changed it on purpose.

## 4. Report

At most eight lines:

- Each task: done, or "needs you" with the exact action and why you could not do it.
- pytest result.
- Files changed.
