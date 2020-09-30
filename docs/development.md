# Development

This is reference material for local development and publishing new versions.

If you just want to use the library, you don't need any of this.

## Release checklist

- Verify tests and examples work. (It must be [passing on Travis CI](https://travis-ci.com/github/jtebert/gridsim).)
- Check that all documentation is updated
- Update version number (`__version__`) in `gridsim/__init__.py`
- Update changelog: move "Unreleased" to new version
- Push to master
- Create release on Github. (This will automatically create a new Stable and version-numbered documentation version on Read The Docs and deploy an updated release to PyPi.)

## Build Documentation

from the `docs` directory, run:

```shell
make html
```

Then open the documentation:

```shell
open _build/html/index.html
```

## Build the distributable for PyPi

(From the [PyPi tutorial](https://packaging.python.org/tutorials/packaging-projects/))

You shouldn't need to do this manually anymore; this will be handled by Travis CI

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

## Profiling code

Use the packages [cProfile](https://docs.python.org/2/library/profile.html) and [cprofilev](https://github.com/ymichael/cprofilev) to profile Python code. This is useful for finding slow spots in the simulator itself, as well as your own user code.

Note that these are not included as dependencies for Gridsim, so you will have to install them yourself:

```shell
pip install cprofilev
```

### Option 1: Using just `cprofilev`

Run your code and profile it at the same time.

```shell
python -m cprofilev main.py test_config.yml
```

### Option 1: Using `cProfile` and `cprofilev`

This saves the output as a file, so you can go back and view it later without having to re-run the code.

1. Run your script and save the output to a log file. For example:
   ```shell
   python -m cProfile -o out_log  main.py test_config.yml
   ```
2. View the output:
   ```shell
   cprofilev -f out_log
   ```
   And go to [localhost:4000](http://localhost:4000) to view the output

