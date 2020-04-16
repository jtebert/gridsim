# Gridsim

*Simple grid-based robot simulator*

**[Documentation](https://gridsim.readthedocs.io/)**

I'm planning on using this as a simple test-bed for my algorithms.

This package will be a package/library for the simulator itself, not the robot code. This follows a similar structure (with a World, Robot, Logger, and Viewer) as Kilosim.

I plan to package this with PyPi so I can easily use it with separate repositories for the algorithms.

For reference on package structure, see the [package-boilerplate](https://github.com/jtebert/package-boilerplate).

## Development

### Build Documentation

from the `docs` directory, run:

```shell
make html
```

Then open the documentation:

```shell
open _build/html/index.html
```

### Build the distributable for PyPi

(From the [PyPi tutorial](https://packaging.python.org/tutorials/packaging-projects/))

Make sure the necessary dependencies are installed.

```shell
pip3 install --upgrade setuptools wheel twine
```

Build the project. From the project root folder, run:

```shell
python3 setup.py sdist bdist_wheel
```

Upload it to the testing index:

```shell
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload it to the actual index:

```shell
python3 -m twine upload dist/*
```