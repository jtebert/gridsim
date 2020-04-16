# __path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .config_parser import ConfigParser
from .message import Message
from .world import World
from .viewer import Viewer
from .robot import Robot
from .logger import Logger

from gridsim.utils import get_version

# Canonical source for version number
# major.minor.patch
VERSION = (0, 1, 2)
