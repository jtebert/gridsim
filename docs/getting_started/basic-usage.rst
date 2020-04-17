.. _basic-usage:

Basic Usage
===========

This will walk you through setting up your first robot and complete simulation.

.. contents:: On this page
  :local:

Test using built in examples
----------------------------

The examples are in the examples directory of the source code. In the near future, I'll set up a way to run the examples directly when you install the package.

Creating a simple robot
-----------------------

For more detailed information about developing custom robots, see :ref:`custom-robot`.

To start, we will only need to make a simple robot based on the :class:`~gridsim.grid_robot.GridRobot`. This needs to implement three methods:

- :meth:`~.robot.Robot.receive_msg`: Code that is run when a robot receives a message
- :meth:`~.robot.Robot.init`: Code that is run once when the robot is created
- :meth:`~.robot.Robot.loop`: Code that is run in every step of the simulation

Create a file for your robot class. Let's call it ``random_robot.py``. Below is a simple Robot that moves randomly and changes direction every 10 seconds. You can copy this or directly download :download:`random_robot.py </../examples/random_robot.py>`

.. literalinclude:: /../examples/random_robot.py
  :language: Python3
  :linenos:


A minimal simulation example
----------------------------

To run a simulation, you need to create a couple of robots, place them in a :class:`~gridsim.world.World`. Then you call the :meth:`~gridsim.world.World.step` method to execute you simulation step-by-step. :meth:`~gridsim.world.World.step` will handle running all of the robots' code, as well as communication and movement.

Use the code below or download :download:`minimal_simulation.py </../examples/minimal_simulation.py>`.

.. literalinclude:: /../examples/minimal_simulation.py
  :language: Python3
  :linenos:


Adding the Viewer
-----------------

With that simple example, you have no way to see what the robots are doing. For that, we add a :class:`~gridsim.viewer.Viewer`. This requires adding only two lines of code to our minimal simulation above.

Use the code below or download :download:`viewer_simulation.py </../examples/viewer_simulation.py>`.

.. literalinclude:: /../examples/viewer_simulation.py
  :language: Python3
  :linenos:
  :emphasize-lines: 20-21,29-30

Notice that adding the Viewer slows down the time to complete the simulation, because the display rate of the Viewer limits the simulation rate. If you want to run lots of simulations, turn off your Viewer.

Using configuration files
-------------------------

TODO: Coming soon

- Show YAML configuration file
- Loading/using configuration values in your function

Logging data
------------

TODO: Coming soon

- Show logging config, individual parameters (and exclude, and that you can't log all types -- see class documentation)
- Show add_aggregator + log_state
- Point to Logger documentation for what the output file looks like and more details about what can be logged/saved

Complete example
----------------

Most simulations will involve all of these components, and multiple trials. You can download a complete, detailed example here: :download:`complete_simulation.py </../examples/complete_simulation.py>`, as well as a corresponding YAML configuration file: :download:`ex_config.yml </../examples/ex_config.yml>`
