.. _custom-robot:

===================
Make your own Robot
===================

.. note::
  This assumes familiarity with object-oriented programming (particularly inheritance and abstract classes).

The Gridsim library provides a :mod:`~gridsim.robot.Robot` class that manages underlying behavior and drawing of robots, making it easy for you to quickly implement your own functionality and algorithms.

In fact, the default ``Robot`` class is an abstract class; you must *implement* your own ``Robot`` subclass. There are five abstract ``Robot`` methods that you must implement in your own class. (Inputs and outputs are not shown.)

- :meth:`~robot.Robot.move`: Step-wise movement of the robot on the grid
- :meth:`~.robot.Robot.comm_criteria`: Distance-based criteria for whether or not another robot is within communication range of this robot.
- :meth:`~.robot.Robot.receive_msg`: Code that is run when a robot receives a message
- :meth:`~.robot.Robot.init`: Code that is run once when the robot is created
- :meth:`~.robot.Robot.loop`: Code that is run in every step of the simulation

It also includes an optional method you may want to implement in your subclass:

- :meth:`~.robot.Robot.msg_received`: Code that is run when a robot's successfully sends a message to another robot.

In general, you will likely want to implement your own robots with an additional *two* layers of subclasses, as seen in the graph below. This allows you to separate the physical robot platform you are representing from the algorithms/code you are running on that platform.

.. graphviz::
  :align: center

  digraph example {
    rankdir="BT"
    robot [label="gridsim.Robot", href="http://sphinx-doc.org", target="_top" shape="record"];
    gr [label="gridsim.GridRobot" shape="record"];
    yr [label="{YourRobot|Custom Robot}" shape="record"];
    ar [
      label="{YourAlgorithm|YourRobot running custom algorithm}"
      shape="record"];
    rr [label="{RandomRobot|GridRobot doing random movement}"
        shape="record"];
    cr [label="{AnotherAlgorithm|GridRobot running different code}"
        shape="record"];

    yr -> robot;
    gr -> robot;
    rr -> gr;
    cr -> gr;
    ar -> yr;

    subgraph cluster_subs {
      label="Robot Platforms"
      rank="same"
      yr
      gr
    }
  }

|

First, you create a subclass that represents the physical robot system you are representing (such as a `Turtlebot <https://www.turtlebot.com/>`_ or `Kilobot <https://www.k-team.com/mobile-robotics-products/kilobot>`_). This is still an abstract class. It implements abstract methods that are properties of the physical system, such as the communication range (:meth:`~.robot.Robot.comm_criteria`) and movement restrictions (:meth:`~robot.Robot.move`). Gridsim include the :class:`~gridsim.grid_robot.GridRobot` as a simple robot platform. You can also create your down, as in the ``YourRobot`` above.

Second, you create a subclass of your new class for implementing specific algorithms or code on your new robot platform. Here you will implement message handling (:meth:`~.robot.Robot.receive_msg` and optionally :meth:`~.robot.Robot.msg_received`) and onboard code (:meth:`~.robot.Robot.init` and :meth:`~.robot.Robot.loop`). You can have multiple subclasses of your platform to run different code on the same platform, such as ``RandomRobot`` (created below as an example) and ``AnotherAlgorithm``.

Custom robot example
====================

Below is an example of the structure described above to create a simple robot that bounces around the arena.

First, we create , a robot with a circular communication radius of 5 grid cells that can move in the cardinal directions to any of four cells surrounding it. This robot is already provided in the library as :class:`~gridsim.grid_robot.GridRobot`; you need not re-implement this robot platform if it meets your needs.

.. literalinclude:: /../gridsim/grid_robot.py
  :language: Python3
  :linenos:

With our robot platform in place, we can now implement a Robot that implements whatever code we want the robot to run. In this case, it's a simple robot that chooses a random movement every 10 ticks. Its color is based on the color it samples at its current location, and whether it has communicated with another robot.

.. literalinclude:: /../examples/random_robot.py
  :language: Python3
  :linenos:

Notice that the abstraction layers mean that you have to write very little additional code to implement a new algorithm for your robot.