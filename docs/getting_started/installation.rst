============
Installation
============

.. note::
    This assumes that you're already familiar with virtual environments and pip.

Virtual Environment Setup
=========================

Create a Python 3 virtual environment in the current location in subfolder called ``venv``, then set it as the Python source.

.. code-block:: console

    $ python3 -m venv venv
    $ source venv/bin/activate

You can deactivate the virtual environment with ``deactivate``.

Quick Install
=============

This package is available through pip, so it's easy to install. With your virual environment active, run:

.. code-block:: console

    $ pip install gridsim

Within your own code, you can now import the Gridsim library components, such as:

.. code-block:: python3

    import gridsim as gs

    # Create an empty World of 100 x 100 grid cells
    my_world = gs.World(100, 100)