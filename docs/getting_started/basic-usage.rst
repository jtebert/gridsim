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

We also want give our Robots something to sense by adding en environment to the World. An environment here is represented with an image. (You'll see what this looks like in the next step.) In each cell, the Robots can sense the color of the cell (i.e., the RGB pixel value) at that location with the :meth:`~gridsim.robot.Robot.sample` method. If you set up the environment with an image whose resolution doesn't match the grid dimensions, it will be rescaled, possibly stretching the image. To avoid any surprises, you should use an image whose resolution matches your grid dimensions (e.g., for a 50 × 50 grid, use a 50px × 50px image).

Use the code below or download :download:`minimal_simulation.py </../examples/minimal_simulation.py>` and the example environment :download:`ex_env.png </../examples/ex_env.png>`.

.. literalinclude:: /../examples/minimal_simulation.py
  :language: Python3
  :linenos:

With these files and ``random_robot.py`` in the same directory, and ``gridsim`` installed, you should be able to run the code with:

.. code-block:: console

  $ python3 minimal_simulation.py

Adding the Viewer
-----------------

With that simple example, you have no way to see what the robots are doing. For that, we add a :class:`~gridsim.viewer.Viewer`. This requires adding only two lines of code to our minimal simulation above.

Use the code below or download :download:`viewer_simulation.py </../examples/viewer_simulation.py>`.

.. literalinclude:: /../examples/viewer_simulation.py
  :language: Python3
  :linenos:
  :emphasize-lines: 22-23, 30-31

Notice that adding the Viewer slows down the time to complete the simulation, because the display rate of the Viewer limits the simulation rate. If you want to run lots of simulations, turn off your Viewer.

Using configuration files
-------------------------

Gridsim also provides the :class:`~gridsim.config_parser.ConfigParser` for using YAML configuration files. This simplifies loading parameters and (as described in the next section) saving parameters with simulation results data.

The :class:`~gridsim.config_parser.ConfigParser` is un-opinionated; it doesn't place any restrictions on what your configuration files look like, as long as they're valid YAML files.

Compared to our ``minimal_simulation.py``, we only need one line to create our :class:`~gridsim.config_parser.ConfigParser`, from which we can retrieve any parameter values.

Use the code below or download :download:`config_simulation.py </../examples/config_simulation.py>` and YAML configuration file :download:`simple_config.yml </../examples/simple_config.yml>`.

.. literalinclude:: /../examples/config_simulation.py
  :language: Python3
  :linenos:
  :emphasize-lines: 7-13, 17-18, 20-21

Logging data
------------

Gridsim has a built-in :class:`~gridsim.logger.Logger`, designed to easily save data from your simulations to HDF5 files. This allows you to store complex data and simulation configurations together in one place. HDF5 files are also easy to read and write in many different programming languages.

There are three main ways to save data to your log files:

- Save the parameters in your configuration with :meth:`~gridsim.logger.Logger.log_config`. (Note that not all data types can be saved with ``log_config``. See its documentation for more details.)
- Save a single parameter (that's not in your configuration file) with :meth:`~gridsim.logger.Logger.log_param`
- Save the state of your simulation/robots with :meth:`~gridsim.logger.Logger.log_state`. (This requires some setup.)

In order to log the state of the World, you first need to tell the :class:`~gridsim.logger.Logger` *what* you want to save about the :class:`~gridsim.robot.Robot`s with an aggregator function. This is a function that takes in a list of Robots and returns a 1D numpy array. Then, whenever you call :meth:`~gridsim.logger.Logger.log_state`, this function is called and the result is added to your dataset. You can add as many aggregators as you want, each with their own name.

We can extend our ``config_simulation.py`` to show the three types of logging described above. Use the code below or download :download:`logger_simulation.py </../examples/logger_simulation.py>`.

.. literalinclude:: /../examples/logger_simulation.py
  :language: Python3
  :linenos:
  :emphasize-lines: 2-4, 9-18, 41-52, 59-60

Complete example
----------------

Most simulations will involve all of these components, and multiple trials. You can download a complete, detailed example here: :download:`complete_simulation.py </../examples/complete_simulation.py>`, as well as a corresponding YAML configuration file: :download:`ex_config.yml </../examples/ex_config.yml>`

Here, the configuration file is used as a command line argument, so it's easy to switch what configuration file you use. Run it like this:

.. code-block:: console

  $ python3 complete_simulation.py ex_config.yml