# ShellForm

**The carbon cost of seismic resilience: gravity-only versus seismic-aware form-finding of concrete shells.**

How much embodied carbon does seismic resilience cost in a form-found concrete shell, and does form-finding that includes seismic loads deliver it more cheaply than thickening a gravity-only shape?

ShellForm extends the seismic form-finding of Michiels & Adriaenssens (2017, 2018) by sizing each form to pass code checks and counting its A1-A3 embodied carbon. It is built on the validated, tagged modules of [ShellBench](https://github.com/syednafizreja/ShellBench) and never copies a ShellBench value (see [docs/data_contract.md](docs/data_contract.md)).

## Status

Day 0 (28 Oct 2026): repository structure. Pinned to ShellBench `v0.0.1` until `floor-r1` lands.

| Item | Where | Status |
|---|---|---|
| Pre-registration | [docs/preregistration.md](docs/preregistration.md) | Draft, awaiting author approval |
| Seismic-aware form-finding | `src/shellform/` | Waits for ShellBench `floor-r1` |
| Tests S1-S5 | `tests/` | Not started |
| 168 sized designs | `results/` | Not started |
| Design explorer | [explorer/index.html](explorer/index.html) | Skeleton, dummy data |

## Design space

2 spans (10, 20 m) x 2 supports (4 corners, continuous edges) x 3 rise-to-span ratios (0.10, 0.15, 0.20) x 2 strategies (gravity-only, seismic-aware) x 7 plateau spectral accelerations (0-0.6 g) = 168 sized designs.

## Setup

```powershell
conda activate research
cd C:\Users\ASUS\ShellBench; git fetch --tags; git checkout v0.0.1   # the tag in src/shellform/pin.py
pip install -e C:\Users\ASUS\ShellBench --no-deps
cd C:\Users\ASUS\ShellForm
pip install meshio
pip install -e . --no-deps
pytest
```

## Licence

MIT. Cite with [CITATION.cff](CITATION.cff).
