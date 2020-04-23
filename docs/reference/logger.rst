======
Logger
======

The logger provides an interface for easily saving time series data from many simulation trials, along with the parameters used for the simulation.

Data is logged in `HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_ (Hierarchical Data Format) files.

Data is stored by trial, in a hierarchy like a file structure, as shown below. Values in ``<`` ``>`` are determined by what you actually log, but the ``params`` group and ``time`` dataset are always created.

::

    log_file.h5
    ├── trial_<1>
    │   ├── params
    │   │   ├── <param_1>
    │   │   ├── <param_2>
    │   │   ├── ⋮
    │   │   └── <param_n>
    │   ├── time
    │   ├── <aggregator_1>
    │   ├── <aggregator_2>
    │   ├── ⋮
    │   └── <aggregator_n>
    ├── trial_<2>
    │   └── ⋮
    ├── ⋮
    └── trial_<n>

All values logged with :meth:`~gridsim.logger.Logger.log_param` and :meth:`~gridsim.logger.Logger.log_config` are saved in ``params``.

Time series data is stored in datasets directly under the ``trial_<n>`` group. They are created by :meth:`~gridsim.logger.Logger.add_aggregator`, and new values are added by :meth:`~gridsim.logger.Logger.log_state`. Calling this method also adds a value to the ``time`` dataset, which corresponds to the :class:`~gridsim.world.World` time at which the state was saved.

.. autoclass:: gridsim.logger.Logger
   :members: