# Handoff between Claude in the app and Claude Code in VS Code

Newest entry first. Each Claude reads this at the start of a session and adds an entry at the end (see "Sync with cloud Claude" in CLAUDE.md).

## 28 Oct 2026, Claude Code in VS Code (Day 0 environment and repo)

**Done:** `shellform` env has ShellBench installed from `C:\Users\ASUS\ShellBench-pin` (`v0.0.1`) and ShellForm in editable mode; `pytest` 2 passed; `check_pin()` returns `v0.0.1`. `research` points back at `C:\Users\ASUS\ShellBench`. Stray uv `.venv` (Python 3.15) deleted; VS Code interpreter set to `shellform`. Repo: README rewritten; `environment.yml` (versions read from the installed env); `.github/workflows/tests.yml` (reads the tag from `pin.py`, checks out ShellBench with secret `SHELLBENCH_DEPLOY_KEY`) and `release.yml` (same as ShellBench's); PR template with the code-standards checklist; `.gitattributes`; `.editorconfig`; `pyproject.toml` Issues link. GitHub: description, six topics, Projects off, branches deleted on merge.

**Decisions by the author today:** setup finished; start Day 1 tomorrow.

**Open (author):**
- Add the CI deploy key (Claude Code was not permitted to). Until then the Tests workflow fails at "Check out ShellBench". In PowerShell:
  `ssh-keygen -t ed25519 -N '""' -C "Shellform CI read-only" -f $env:TEMP\sb_deploy`
  `gh repo deploy-key add $env:TEMP\sb_deploy.pub -R syednafizreja/ShellBench -t "Shellform CI (read-only)"`
  `Get-Content $env:TEMP\sb_deploy -Raw | gh secret set SHELLBENCH_DEPLOY_KEY -R syednafizreja/Shellform`
  `Remove-Item $env:TEMP\sb_deploy, $env:TEMP\sb_deploy.pub`
  Then re-run the failed workflow and merge PR `day00-repo`.
- Items from the app entry below are unchanged.

**Next:** Day 1 (29 Oct), Michiels 2017 reading notes and pre-registration approval.

## 28 Oct 2026, Claude in the app (Day 0 scaffold)

**Done:** repository structure; `src/shellform/pin.py` pins ShellBench `v0.0.1` (the only tag today); `docs/data_contract.md` copied from the project file `10_ShellForm_Reference_Data.md`; draft `docs/preregistration.md` from contract sections 3-4; `explorer/index.html` skeleton (three.js, dummy data, labelled as such); smoke tests.

**Decisions by the author today:** start ShellForm on 29 Oct; build ends 13 Nov; check window 14-17 Nov.

**Open (author):**
- Approve or change `docs/preregistration.md`. It must be committed before any run.
- Get the four Michiels & Adriaenssens papers (test S4 depends on them).
- Send ShellBench "What ShellForm needs" (contract section 6) by Mon 2 Nov.
- Read GB 50011 Table 5.1.4-1 design and rare alpha_max, and an EN 1998-1 example site, before they become plot markers [?].

**Next:** Day 1 (29 Oct), Michiels 2017 reading notes and pre-registration approval.
