====================
Configuration Parser
====================

The ``ConfigParser`` is an optional class to help separate your code for experimental configurations by using `YAML <https://yaml.org/>`_ files for configuration. This imposes very few restrictions on the way you set up your configuration files; it mostly makes it easier to access their contents and save the configuration parameters with your data using the :class:`~gridsim.logger.Logger`.

This is useful for managing both values that are fixed through all experiments (e.g., dimensions of the arena) and experimental values that vary between conditions (e.g., number of robots). The latter may be saved as an array and a single value used for different conditions.

While the ``ConfigParser`` can load any valid YAML files, the largest restriction is what configuration parameter types can be saved to log files. For details, see the :meth:`~gridsim.logger.Logger.log_config` documentation.

.. autoclass:: gridsim.config_parser.ConfigParser
    :members: