======
Viewer
======

The Viewer is a simple way to visualize your simulations. After creating the Viewer, just call  :meth:`~gridsim.viewer.Viewer.draw` each step (or less frequently) to see the current state of the World.

.. note::
   The maximum Viewer refresh rate (set at creation with the ``display_rate`` argument) also limits the simulation rate. If you want to run faster/higher-throughput simulations, don't use the Viewer, or make it draw less frequently than every tick.

.. autoclass:: gridsim.viewer.Viewer
   :members:

