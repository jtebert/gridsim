from typing import Tuple, Optional


def get_version(version: Optional[Tuple[int, int, int]] = None) -> str:
    """
    Return main version (X.Y[.Z]) from VERSION (found in __init_).

    Parameters
    ----------
    version : Optional[Tuple[int, int, int]], optional
        Custom version to use, by default None. If not specified, this will use the version
        (VERSION) specified in gridsim/__init__.py

    Returns
    -------
    str
        String representation of the version "major.minor[.patch]"
    """
    if version is None:
        from gridsim import VERSION as use_version
    else:
        assert len(version) == 3
        use_version = version

    parts = 2 if use_version[2] == 0 else 3
    return '.'.join(str(x) for x in use_version[:parts])
