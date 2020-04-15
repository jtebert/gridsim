"""
For logging data out of the simulator (probably as HDF5, but TBD)
"""

from typing import Optional, Callable, List, Dict, Union
import os
import re

import h5py
import numpy as np

from .world import World
from .robot import Robot
from .config_parser import ConfigParser


class Logger:
    # Allowed parameter datatypes (from configuration) that can be logged
    PARAM_TYPE = Union[str, int, float, bool, list]
    # Mapping between Python datatypes and h5py/HDF5 datatypes
    DATATYPE_MAP = {
        str: h5py.string_dtype(),  # http://docs.h5py.org/en/stable/strings.html
        int: 'int64',
        float: 'float64',
        bool: np.bool,
        list: 'float64',
    }

    @staticmethod
    def type_str(type_v):
        return re.findall(r"'(.*?)'", str(type_v))[0]

    def __init__(self, world: World, filename: str, trial_num: int,
                 overwrite_trials: Optional[bool] = False):
        """
        Create a Logger to save data to an HDF5 file, from a single simulation
        trial.

        Note that this only creates the Logger with which you can save data. You
        must use the methods below to actually save anything to the file with
        the Logger.

        Parameters
        ----------
        world : World
            World whose simulation data you want to save.
        filename : str
            Name of the HDF5 file to save data to (``.hdf`` extension). If the
            file does not exist, it will be created. If it does exist, it will
            be appended to (with the overwriting caveat specified below)
        trial_num : int
            Trial number under which to save the data.
        overwrite_trials : Optional[bool], optional
            Whether to overwrite a trial's data if it already exists, by default
            False
        """
        self._world = world
        self._filename = filename
        self._trial_num = trial_num
        self._overwrite_trials = overwrite_trials
        self._log_file = h5py.File(filename, 'a')

        self._trial_group_name = "trial_{}".format(trial_num)
        self._params_group_name = os.path.join(self._trial_group_name, 'params')
        self._time_dset_name = os.path.join(self._trial_group_name, 'time')
        self._set_trial()

        self._aggregators: Dict[str, Callable[[List[Robot]], np.ndarray]] = {}

    def _set_trial(self):
        # Create group for the trial
        if self._trial_group_name in self._log_file:
            if self._overwrite_trials:
                # Delete previous trial group
                del self._log_file[self._trial_group_name]
                print("WARNING: Overwrote trial {} data"
                      .format(self._trial_num))
            else:
                raise ValueError('Conflicts with existing trial {}. '
                                 .format(self._trial_num) +
                                 'Exiting to avoid data overwrite')
        self._log_file.create_group(self._trial_group_name)

        # Create the params group, if it doesn't already exist
        self._log_file.create_group(self._params_group_name)

        # Create a packet table dataset for the timeseries
        # http://docs.h5py.org/en/stable/faq.html#appending-data-to-a-dataset
        self._log_file.create_dataset(self._time_dset_name,
                                      shape=(0,),
                                      maxshape=(None,), dtype='float64')

    def get_trial(self) -> int:
        """
        Get the trial number that this Logger is logging

        Returns
        -------
        int
            Number of the current trial being logged
        """
        return self._trial_num

    def add_aggregator(self, name: str,
                       func: Callable[[List[Robot]], np.ndarray]):
        """
        Add an aggregator function that will map from the list of all Robots in
        the world to a 1D array of floats. This will be used for logging the
        state of the World; the output of the aggregator is one row in the
        HDF5 Dataset named with the ``name``.

        The function reduces the state of the Robots to a single or multiple
        values. It could map to one float per robot (such as a state variable of
        each Robot) or a single value (length 1 array, such as an average value
        over all Robots).

        Because of Python's dynamic typing, this does not validate whether the
        subclass of Robot has any parameters or functions that are called by the
        aggregator. The user is responsible for adding any necessary checks in
        the aggregator function.

        Notes
        -----
        The width of the aggregator table is set when this function is called,
        which is determined by the length of the output of ``func``. If the length
        depends on the number of Robots, all Robots should be added to the
        ``World`` *before* adding any aggregators to the ``Logger``.

        The aggregator ``func`` will be applied to all robots in the world,
        regardless of type. However, if you have multiple types of Robots in
        your ``World``, you can make an aggregator that applies to one type by
        filtering the robots by type within the ``func``.

        Parameters
        ----------
        name : str
            Key that will be used to identify the aggregator results in the HDF5
            log file.
        func : Callable[[List[Robot]], np.ndarray]
            Function that maps from a list of Robots to a 1D array to log some
            state of the Robots at the current time.
        """
        # Add the function to the aggregators to be called for logging the state
        self._aggregators[name] = func

        # Do a test run of the aggregator to get the length of the output
        test_output = func(self._world._robots.sprites())
        out_size = test_output.size
        # Should be 1D array (size is a single integer)
        if not isinstance(out_size, int):
            raise ValueError(
                "Aggregator {} must return a 1D array".format(name))
        agg_dset_name = os.path.join(self._trial_group_name, name)
        # Setting the max_shape with None allows for resizing to add data
        self._log_file.create_dataset(agg_dset_name,
                                      shape=(0, out_size),
                                      maxshape=(None, out_size),
                                      dtype='float64')

    def log_state(self):
        """
        Save the output of all of the aggregator functions. If you have not
        added any aggregators with :meth:`~gridsim.logger.Logger.log_state`,
        nothing will be saved by this function.

        The runs each previously-added aggregator function and appends the
        result to the respective HDF5 Dataset. It also saves the current time of
        the World to the ``time`` Dataset.
        """
        # Add the time
        time = self._world.get_time()
        self._log_file[self._time_dset_name].resize(
            (self._log_file[self._time_dset_name].shape[0] + 1),
            axis=0)
        self._log_file[self._time_dset_name][-1:] = time

        # Add the output of each aggregator function
        robots = self._world._robots.sprites()
        for name, func in self._aggregators.items():
            agg_vals = func(robots)
            dset_name = os.path.join(self._trial_group_name, name)
            self._log_file[dset_name].resize(
                (self._log_file[dset_name].shape[0] + 1),
                axis=0
            )
            self._log_file[dset_name][-1:] = agg_vals

    def log_config(self, config: ConfigParser):
        """
        Save all of the parameters in the configuration.

        Notes
        -----
        Due to HDF5 limitations (and my own laziness), only the following
        datatypes can be saved in the HDF5 parameters:

        - string
        - integer
        - float
        - boolean
        - list of integers and/or floats

        Parameters
        ----------
        config : ConfigParser
            Configuration loaded from a YAML file.
        """
        params = config.get()

        for name, val in params.items():
            self.log_param(name, val)

    def log_param(self, name: str, val: PARAM_TYPE):
        """
        Save a single parameter value. This is useful for saving fixed
        parameters that are not part of your configuration file, and therefore
        not saved with :meth:`~gridsim.logger.Logger.log_config`.

        Parameters
        ----------
        name : str
            Name/key of the parameter value to save
        val : Any
            Value of the parameter to save. This can be a
        """
        dset_name = os.path.join(self._params_group_name, name)
        v_type = type(val)
        if isinstance(val, list):
            # Check that it's a list of floats or ints
            all_floats = all(map(
                lambda v: isinstance(v, int) or isinstance(v, float),
                val))
            if not all_floats:
                # raise ValueError('Can only log lists of ints and floats')
                print('WARNING: Can only save lists of ints and floats. ' +
                      'Skipping parameter "{}"'
                      .format(name))
                return
        try:
            dtype = Logger.DATATYPE_MAP[v_type]
        except KeyError:
            # raise ValueError("""Cannot process '{}' data.
            #  Can only process data of types: {}
            #     """.format(
            #     Logger.type_str(v_type),
            #     list(map(Logger.type_str,
            #              Logger.DATATYPE_MAP.keys()))))
            print('WARNING: Cannot save {} data. Skipping parameter "{}"'
                  .format(Logger.type_str(v_type), name))
            return
        self._log_file.create_dataset(dset_name, data=val, dtype=dtype)
