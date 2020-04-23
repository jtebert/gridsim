from typing import Any, Optional

import yaml


class ConfigParser:
    """
    Class to handle YAML configuration files.

    This can be directly passed to the :meth:`~gridsim.logger.Logger.log_config`
    to save all configuration values with the trial data.
    """

    def __init__(self, config_filename: str):
        """
        Create a configuration parser to manage all of the parameters in a YAML
        configuration file.

        Parameters
        ----------
        config_filename : str
            Location and filename of the YAML config file
        """
        with open(config_filename) as f:
            self._params = yaml.load(f, Loader=yaml.FullLoader)

    def get(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get a parameter value from the configuration, or get a dictionary of the
        parameters if no parameter name (key) is specified.

        Note that if no default is specified and the key is *not* found in the
        configuration file, this will return ``None`` instead of rasing an
        exception.

        Parameters
        ----------
        key : Optional[str], optional
            Name of the parameter to retrieve, by default None. If not
            specified, a dictionary of all parameters will be returned.
        default : Any, optional
            Default value to return if the key is not found in the
            configuration, by default None

        Returns
        -------
        Any
            Parameter value for the given key, or the default value is the key
            is not found. If no key is given, a dictionary of all parameters
            is returned.
        """
        if key is None:
            return self._params
        else:
            return self._params.get(key, default)
