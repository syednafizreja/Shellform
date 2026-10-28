"""Smoke tests: the package imports and ShellBench matches the pin."""


def test_import_shellform():
    """Import the package and check it exposes a version string."""
    import shellform

    assert isinstance(shellform.__version__, str)


def test_shellbench_matches_pin():
    """The installed shellbench is the pinned release."""
    from shellform.pin import SHELLBENCH_TAG, check_pin

    assert check_pin() == SHELLBENCH_TAG
