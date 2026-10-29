"""Tests for the design space and results columns."""

from shellform.design_space import RESULT_COLUMNS, design_space


def test_full_space_has_168_unique_cases():
    cases = design_space()
    assert len(cases) == 168
    assert len({c["design_id"] for c in cases}) == 168


def test_stop_loss_space_has_84_cases():
    assert len(design_space(spans=(10.0,))) == 84


def test_every_result_names_the_shellbench_tag():
    assert "shellbench_tag" in RESULT_COLUMNS
    assert len(set(RESULT_COLUMNS)) == len(RESULT_COLUMNS)
