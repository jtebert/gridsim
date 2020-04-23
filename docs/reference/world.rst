=====
World
=====

The World is where all of the simulation happens. Robots are added to the World, and the Viewer and Logger refer to a World to draw the simulation and save data.

Once the World is created and you have added your robots, you will likely only need to call the :meth:`~gridsim.world.World.step` method.

.. autoclass:: gridsim.world.World
   :members:
   :exclude-members: has_new_environment, get_environment