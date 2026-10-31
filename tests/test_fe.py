"""Tests for the CalculiX shell analysis (skipped where ccx is not installed).

Material inputs here are test inputs for the solver, not ShellBench values;
design runs take them from ShellBench at the pinned tag.
"""

import numpy as np
import pytest

from shellform.fe import analyse, find_ccx, parse_dat, s8r_elements, surface_area
from shellform.formfind import corner_network_for_inset, form_to_rise, square_network

needs_ccx = pytest.mark.skipif(find_ccx() is None, reason="CalculiX not on PATH")
E_TEST, NU_TEST, RHO_TEST = 3.0e10, 0.2, 2400.0


def test_s8r_mesh_covers_grid():
    els = s8r_elements(5)
    assert els.shape == (4, 8)
    assert len(np.unique(els)) == 21  # 25 grid nodes less 4 unused element centres


def test_flat_grid_area():
    net = square_network(10.0, 11, "edges")
    assert surface_area(net.xyz, 11) == pytest.approx(100.0)


def test_parse_dat_reads_buckling_factors():
    text = " B U C K L I N G   F A C T O R   O U T P U T\n\n MODE NO       BUCKLING\n                FACTOR\n\n      1   0.7618208E+00\n      2   0.1336737E+01\n\n"
    assert np.allclose(parse_dat(text)[3], [0.7618208, 1.336737])


@needs_ccx
def test_corner_supported_shell_reactions_equal_weight(tmp_path):
    net, xyz, _ = corner_network_for_inset(10.0, 21, 1.5, 0.10)
    r = analyse(xyz, 21, net.fixed, 0.08, E_TEST, NU_TEST, RHO_TEST, workdir=tmp_path)
    assert r.reaction_n[2] == pytest.approx(r.weight_n, rel=5e-3)
    assert abs(r.reaction_n[0]) < 1e-3 * r.weight_n and abs(r.reaction_n[1]) < 1e-3 * r.weight_n
    assert len(r.periods_s) == 3 and r.periods_s[0] > 0
    assert r.buckling_factors[0] > 1.0


@needs_ccx
def test_edge_supported_shell_is_stiffer_than_corner_supported(tmp_path):
    out = {}
    for sup in ("edges", "corners"):
        if sup == "edges":
            net = square_network(10.0, 21, "edges")
            xyz = form_to_rise(net, 1.5)
        else:
            net, xyz, _ = corner_network_for_inset(10.0, 21, 1.5, 0.10)
        out[sup] = analyse(xyz, 21, net.fixed, 0.08, E_TEST, NU_TEST, RHO_TEST, workdir=tmp_path / sup)
    assert out["edges"].max_disp_m < out["corners"].max_disp_m
    assert out["edges"].periods_s[0] < out["corners"].periods_s[0]
