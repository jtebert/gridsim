"""
Simulate the grid-based world, full of robots
"""

from typing import Tuple, List, Optional, Dict

import pygame

from .robot import Robot
from .environment import Environment, ImageEnvironment


class World:

    def __init__(self, width: int, height: int,
                 robots: List[Robot] = [],
                 environment: str = '',
                 allow_collisions: bool = True):
        """
        Create a World for simulating Robots in a grid world

        Parameters
        ----------
        width : int
            Width of the world (number of cells)
        height : int
            Height of the world (number of cells)
        robots : List[Robot], optional
            List of Robots to place in the World to start, by default []. Additional robots can be
            added after initialization with the :meth:`~gridsim.world.World.add_robot` method.
        environment : str, optional
            Filename of an image to use for a background in the World. Robots will be able to sense
            the color of this image. If the environment dimensions do not match the World
            dimensions, the image will be re-scaled (and possibly stretched). I recommend using an
            image with the same resolution as your grid size. This supports using ``~`` to indicate
            the user home directory.
        allow_collisions : bool, optional
            Whether or not to allow Robots to exist in the same grid cell, by default True.
        """
        self._grid_width = width
        self._grid_height = height
        self._robots = pygame.sprite.Group()

        self._allow_collisions = allow_collisions
        self._tick = 0

        # Cells that will be tagged (translucent color overlayed) in the Viewer
        # Dictionary of {(x, y) cell: (R, G, B) color}
        # These are set in the tag() method
        self._tagged_pos: Dict[Tuple[int, int], Tuple[int, int, int]] = {}

        # Environment (image background)
        self._environment: Environment = Environment()
        if environment:
            self.add_environment(environment)

        [self.add_robot(r) for r in robots]

    def step(self):
        """
        Run a single step of the simulation. This moves the robots, manages the clock, and runs the
        robot controllers.
        """

        self._robots.update()
        self._communicate()
        self._tick += 1

    def add_robot(self, robot: Robot):
        """
        Add a single robot to the World. Robots can also be added in bulk (as a list) when the
        ``World`` is created, using the ``robots`` keyword.

        Parameters
        ----------
        robot : Robot
            Robot to add to the World
        """
        self._robots.add(robot)
        robot.add_to_world(self._grid_width, self._grid_height, world=self)

    def add_environment(self, img_filename: str):
        """
        Add an image to the environment for the Robots to sense. This will also be shown by the
        Viewer.

        Because sensing is cell-based, images will be scaled to the size of the World's grid. If the
        aspect ratio does not match, images will be stretched. To avoid any surprises from
        rescaling, I recommend using an image with the same resolution as your grid size. (e.g., if
        you have a 50x50 grid, use a 50px x 50px image.)

        Parameters
        ----------
        img_filename : str
            Filename of the RGB image to use as a background environment. Any transparency (alpha)
            is ignored by the robot sensing.
        """
        # Add an image as an environment
        self._environment = ImageEnvironment(
            img_filename,
            (self._grid_width, self._grid_height))
        # Make sure all the Robots have the environment information
        for r in self._robots:
            r._environment = self._environment

    def has_new_environment(self):
        """
        [For the Viewer]: Does the World have a new Environment since the last time that the World
        was drawn?

        Returns
        -------
        bool
            Whether the Environment has been used by the Viewer since it was added to the World
        """
        return not self._environment.is_in_viewer

    def get_environment(self) -> Environment:
        """Get the Environment representation for this World

        Returns
        -------
        Environment
            Representation of the Environment
        """
        return self._environment

    def _communicate(self):
        """
        Run all pairwise communication of robots from broadcast messages.

        This checks that the receiving robots are of the right type (specified by the Mesage), and
        that robots are within mutual communication range of each other.
        """
        # (Slow) loop through all robot pairs
        for tx_r in self._robots:  # transmitting robot
            msg = tx_r.get_tx_message()
            if msg:  # only transmit non-empty messages
                for rx_r in self._robots:  # receiving robot
                    # Receiver must be target type (and not itself)
                    if tx_r != rx_r and isinstance(rx_r, msg._rx_type):
                        dist = tx_r.distance(rx_r.get_pos())
                        if tx_r.comm_criteria(dist) and \
                                rx_r.comm_criteria(dist):
                            # Receiving robot processes incoming message
                            rx_r.receive_msg(msg, dist)
                            # Tell sender that the message was received
                            tx_r.msg_received()

    def get_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions (in grid cells) of the World

        Returns
        -------
        Tuple[int, int]
            (width, height) of the World, in grid cells
        """
        return self._grid_width, self._grid_height

    def get_time(self) -> float:
        """
        Get the current time of the World. At the moment, that's just the number of ticks (time
        steps) since the simulation started, since this is a discrete-time world.

        Returns
        -------
        float
            Number of ticks (steps) since simulation started
        """
        return self._tick

    def get_robots(self) -> pygame.sprite.Group:
        """
        Get a list of all the robots in the World

        Returns
        -------
        pygame.sprite.Group
            All Robots currently in the World
        """
        return self._robots

    def tag(self, pos: Tuple[int, int], color: Tuple[int, int, int]):
        """
        Tag a cell position in the World with an RGB color to display in the viewer. There will be a
        semi-transparent overlay with the given color in that cell in the World. This is primarily
        for use with the Viewer, to visualize what has been sampled in the World.

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position to mark
        color : Tuple[int, int, int]
            (R, G, B) color to set as the cell's overlay color (each in the range [0, 255])
        """
        if all([0 <= c <= 255 for c in color]):
            self._tagged_pos[pos] = color
        else:
            raise ValueError('RGB values must all be in the range [0, 255]')
