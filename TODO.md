# TODO

## Code

- Fix the fact that Viewer/Logger (and maybe other things?) refer to the private `_robots` member.
- Add tests
- Add sensing + something to sense
  - Also, do Robots get to know world dimensions so they can avoid hitting the edge?

## Extras

- Documentation
  - Add class descriptions in .py files
  - Write "Basic Usage" page
- Continuous integration
  - Add Travis CI to run test
  - [Travis for PyPi deployment](https://docs.travis-ci.com/user/deployment/pypi/)
- Figure out how to keep version numbering synchronized
  - In `setup.py` (pip), Git/Github releases, and `docs/conf.py`
  - From looking at Wagtail ([conf.py](https://github.com/wagtail/wagtail/blob/v2.8.1/docs/conf.py) and [wagtail/\_\_init\_\_.py](https://github.com/wagtail/wagtail/blob/v2.8.1/wagtail/__init__.py)), perhaps there is one location that keeps a canonical version and all the other files import that.