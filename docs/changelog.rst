=========
Changelog
=========

This documents changes for each Gridsim release. These can also be found with each `Github release <https://github.com/jtebert/gridsim/releases>`_.

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. contents:: Versions
  :local:
  :depth: 1

Unreleased (probably v0.5)
==========================

Added
-----

- :class:`~gridsim.world.World` now has the capability for probabilistic observations. For more information, see the World constructor documentation.
- New method :meth:`~gridsim.world.World.count_tags` returns the number of tagged locations in the world
- :class:`~gridsim.logger.Logger` now supports logging dictionary parameters (including those saved from config files).
- When logging parameters with :meth:`~gridsim.logger.Logger.log_param`, you can now specify a subgroup of ``params`` in which to save the data.
- :class:`~gridsim.message.Message` now has a method :meth:`~gridsim.message.Message.set_all` to replace the whole contents of the Message without creating a new message. (And as opposed to setting the contents key-by-key with :meth:`~gridsim.message.Message.set_all`.)
- Documentation for profiling code (under Development)
- Option in Viewer initialization to draw time as text within window
- Option in Viewer initialization to draw the communication network between robots

Changed
-------

- :meth:`~gridsim.robot.Robot.comm_criteria` and :meth:`~gridsim.robot.Robot.receive_msg` now have an argument of `dist_sqr` instead of `dist`. This is because the square root call in computing the distance is computationally expensive and is called for communication (an N^2) operation.
- For :meth:`~gridsim.world.World.tag`, you can now pass ``None`` instead of a color to remove an existing tag.
- [Under the hood] Convert World tagging to use 3D numpy array instead of list of Tuples. This also improves drawing speed ( it doesn't slow down so much when more tags are added), and you don't get gaps between tagged cells for certain window sizes.
- Improve interpolation for resized environment images
- Improved code documentation.

  - Add documentation of errors and warnings
  - Move constructor documentation from ``__init__`` to class documentation. (I think it looks nicer.)
  - Move documentation from \*.rst to \*.py files, for the sake of having all the documentation in the same place.

Fixed
-----

- You can now no longer :meth:`~gridsim.world.World.tag` cells that are outside of the World dimensions.
- An error is raised when trying to create a :class:`~gridsim.logger.Logger` aggregator (with :meth:`~gridsim.logger.Logger.add_aggregator`) using a reserved name (e.g., ``params`` or ``time``).
- Fix Viewer bug that didn't correctly display background color underneath Robots

`0.4 <https://github.com/jtebert/gridsim/releases/tag/v0.4>`_ (2020-08-20)
==========================================================================

Added
-----

- You can now set the contents of a :class:`~gridsim.message.Message` by key, without needing to create a new message.
- When creating a :class:`~gridsim.config_parser.ConfigParser`, you can now choose to show warnings when getting a value that isn't in the config file
- If a data directory (in the path for a :class:`~gridsim.logger.Logger` filename) does not exist, it will be created.
- New method :meth:`~gridsim.logger.Logger.log_system_info` allows you to easily save information about the system on which the experiments are being run.
- Paths for both :class:`~gridsim.logger.Logger` and :class:`~gridsim.environment.ImageEnvironment` (used via :class:`~gridsim.world.World` support using ``~`` to indicate home directory

Changed
-------

- Trying to have a :class:`~gridsim.robot.Robot` sample outside of the arena now returns ``None``. Previously, this threw a lower-level error about an image index being out of range.
- Decrease :class:`~gridsim.world.World` tag opacity
- Formatting: Changed to 100-character line limit (from 80).
- [Under the hood] Renamed ``WorldEnvironment`` to ``ImageEnvironment``

Fixed
-----

- Previously, if you tried to :meth:`~gridsim.robot.Robot.sample` a negative position in the World, it would loop the index around and give you the value of a position on the other side of the environment. Now, this is considered out of bounds and returns ``None``.
- Improve performance for drawing large number of tags in the :class:`~gridsim.viewer.Viewer` (by converting coordinates to integers).
- Trying to use the :class:`~gridsim.Viewer.Viewer` without an environment image in the World would cause a crash. Now it doesn't.
- Return type and documentation for :meth:`~gridsim.robot.Robot.sample` now matches that of the environment (returns None if sampling outside boundaries).
- Fix broken :func:`~gridsim.utils.get_version` function.
- Time in :class:`~gridsim.logger.Logger` is now stored as an integer (since it's ticks). Previously, it was a float.

`0.3 <https://github.com/jtebert/gridsim/releases/tag/v0.3>`_ (2020-06-29)
==========================================================================

Added
-----

- Grid cells in the World can now be tagged with a color by the :meth:`~gridsim.world.World.tag` method. (The color tag is only used by the :class:`~gridsim.viewer.Viewer` when it draws the World.)
- The Robot's :meth:`~gridsim.robot.Robot.sample` method now includes an option to tag the sampled location in the :class:`~gridsim.world.World` with a color.
- :class:`~gridsim.message.Message` now has "truthiness": null messages are ``False`` and non-null messages are ``True``.
- Messages contents can be accessed by key with the :meth:`~gridsim.message.Message.get` method, as well as still being able to retrieve the entire message dictionary contents.
- Created this changelog

Changed
-------

- ``Message.tx_id()`` has been renamed to the (more informative) :meth:`~gridsim.message.Message.sender`.
- Robot's :meth:`~gridsim.robot.Robot.init` isn't run until the robot is placed in the World. This allows robots to have access to ``World`` information (like the arena size) in the ``init()`` method.
- [Under the hood] World's environments are abstracted to have empty and non-empty types, which cleans up code to get rid of reliance on checking for environments being ``None``.
- [Under the hood] Reduce reliance on cheating and accessing private variables and methods (underscore-prefixed methods/variables)

Removed
-------

- ``Message.is_null`` has been removed. Instead, directly use the boolean conversion described above.

Fixed
-----

- Order of commands run on the robot resulted in incorrect movements (robot-specific :meth:`~gridsim.robot.Robot.move`, then Robot controller/loop function, then collision/environment-aware ``_move`` operation to move the robots which was using a *different* move command)
- Remove mypy/flake8 from requirements, since they're for local development/linting.

`0.2 <https://github.com/jtebert/gridsim/releases/tag/v0.2>`_ (2020-04-20)
==========================================================================

Added
-----

- Worlds now have environments (images) that can be sensed by Robots.
- Documentation has been improved, now with complete instructions for basic setup and usage.