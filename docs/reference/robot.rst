======
Robots
======

Gridsim provides two levels of abstract robot classes. The first, :class:`~gridsim.robot.Robot`, is designed to allow a user full control over their robot platform, specifying to communication criteria and allowed movements.

To get started faster, :class:`~gridsim.grid_robot.GridRobot` implements a simple movement protocol and communication criterion, allowing the user to quickly start implementing their own code on the `GridRobot` platform.

For details on extending the Robot classes to create your own, see :ref:`custom-robot`.

.. autoclass:: gridsim.robot.Robot
   :members:
   :exclude-members: update


.. autoclass:: gridsim.grid_robot.GridRobot
   :members: