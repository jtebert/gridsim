def get_version() -> str:
    """
    Return main version (X.Y[.Z]) from __version__ (found in gridsim/__init__.py).

    Returns
    -------
    str
        String representation of the version "major.minor[.patch]"
    """
    from gridsim import __version__
    return __version__
