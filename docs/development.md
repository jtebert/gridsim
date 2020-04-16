## Development

This is reference material for local development.

If you just want to use the library, you don't need any of this.

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