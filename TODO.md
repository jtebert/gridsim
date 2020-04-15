# TODO

- Make the logger work
  - Add h5py as a dependency in setup.py
- Documentation
  - Add additional information to class reference documentation
  - Add class descriptions in .py files
  - Getting started
    - Add installation instructions (cover HDF5 system dependency)
    - Add example for making your own Robot class
- Add tests
  - And move the current stuff in the tests folder (none of which is actually tests) to somewhere else. (Maybe an examples directory?)
- Continuous integration
  - Add Travis CI to run test
  - [Travis for PyPi deployment](https://docs.travis-ci.com/user/deployment/pypi/)
- Add support for configuration
  - Like Kilosim, but using YAML instead of JSON (and add to setup.py requirements)
- Figure out how to keep version numbering synchronized
  - In `setup.py` (pip), Git/Github releases, and `docs/conf.py`
  - From looking at Wagtail ([conf.py](https://github.com/wagtail/wagtail/blob/v2.8.1/docs/conf.py) and [wagtail/\_\_init\_\_.py](https://github.com/wagtail/wagtail/blob/v2.8.1/wagtail/__init__.py)), perhaps there is one location that keeps a canonical version and all the other files import that.