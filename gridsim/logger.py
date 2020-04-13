"""
For logging data out of the simulator (probably as HDF5, but TBD)
"""

from typing import Optional, Callable, List

import h5py
import numpy as np

from .world import World
from .robot import Robot


class Logger:
    def __init__(self, world: World, filename: str, trial_num: int,
                 overwrite_trials: Optional[bool] = False):
        self._world = world
        self._filename = filename
        self._trial_num = trial_num
        self._overwrite_trials = overwrite_trials
        self._log_file = h5py.File(filename, 'w')
        self._set_trial()

    def _set_trial(self):
        # TODO: Setup logging for this trial
        print('"_set_trial" not implemented yet')

    def log_config(self, config):
        # TODO: Log the parameters in the configuration file
        print('"log_config" not implemented yet')
        pass

    def add_aggregator(self, name: str,
                       func: Callable[[List[Robot]], np.ndarray]):
        # TODO: Add a function that will aggregate state values
        print('"add_aggregator" not implemented yet')
        pass

    def log_state(self):
        # TODO: Log the current state (all aggregators) of all robots
        print('"log_state" not implemented yet')
        pass
