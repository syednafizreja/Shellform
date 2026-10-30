"""The ShellForm design space and the columns of its results table.

The levels below are ShellForm's own choices (docs/data_contract.md,
section 3), pre-registered in docs/preregistration.md section 3. They are
not ShellBench values. Change them only through the pre-registration.
"""

from itertools import product

SPANS_M = (10.0, 20.0)
SUPPORTS = ("corners", "edges")
RISE_RATIOS = (0.10, 0.15, 0.20)
STRATEGIES = ("gravity", "seismic")
SA_LEVELS_G = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)

# One row per sized design. Units in brackets; every row names the
# ShellBench tag it used (CLAUDE.md, code standards).
RESULT_COLUMNS = (
    "design_id",
    "shellbench_tag",
    "span_m",
    "supports",
    "rise_ratio",
    "strategy",
    "sa_g",
    "feasible",
    "thickness_m",
    "concrete_m3",
    "steel_kg",
    "buckling_factor",
    "period_1_s",
    "max_compression_mpa",
    "max_deflection_m",
    "governing_check",
    "t_env_m",
    "carbon_gbt51366_kgco2e",
    "carbon_gbt51366_kgco2e_m2",
)
# The +/-25 % factor band (docs/preregistration.md, decision P3) is
# recomputed from concrete_m3 and steel_kg, so it needs no extra columns.


def design_id(span_m, supports, rise_ratio, strategy, sa_g):
    """Return a stable, readable identifier for one design.

    Example: ``L10-corners-r0.15-seismic-sa0.3``.
    """
    return f"L{span_m:g}-{supports}-r{rise_ratio:.2f}-{strategy}-sa{sa_g:.1f}"


def design_space(spans=SPANS_M):
    """Return every design case as a list of dicts.

    Args:
        spans: Spans to include [m]. The stop-loss rule (drop the 20 m span
            if more than 2 days behind on 6 Nov) passes ``spans=(10.0,)``.

    Returns:
        One dict per case with keys design_id, span_m, supports, rise_ratio,
        strategy and sa_g. 168 cases for the full space.
    """
    cases = []
    for span, sup, rise, strat, sa in product(spans, SUPPORTS, RISE_RATIOS, STRATEGIES, SA_LEVELS_G):
        cases.append({
            "design_id": design_id(span, sup, rise, strat, sa),
            "span_m": span,
            "supports": sup,
            "rise_ratio": rise,
            "strategy": strat,
            "sa_g": sa,
        })
    return cases
