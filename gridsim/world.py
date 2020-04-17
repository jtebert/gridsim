"""
Simulate the grid-based world, full of robots
"""

from typing import Tuple, List

import pygame
from PIL import Image

from .robot import Robot


class World:

    def __init__(self, width: int, height: int,
                 robots: List[Robot] = [],
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
            List of Robots to place in the World to start, by default [].
            Additional robots can be added after initialization with the
            `add_robot` method.
        allow_collisions : bool, optional
            Whether or not to allow Robots to exist in the same grid cell, by
            default True
        """
        self._grid_width = width
        self._grid_height = height
        [r._add_to_world(self._grid_width, self._grid_height) for r in robots]
        self._robots = pygame.sprite.Group(robots)
        self._allow_collisions = allow_collisions
        self._tick = 0

        # Environment (image background)
        self.has_environment = False

    def step(self):
        """
        Run a single step of the simulation. This moves the robots, manages the
        clock, and runs the robot controllers.
        """

        self._robots.update()
        self._communicate()
        self._tick += 1

    def add_robot(self, robot: Robot):
        """
        Add a single robot to the World. Robots can also be added in bulk (as a
        list) when the ``World`` is created, using the ``robots`` keyword.

        Parameters
        ----------
        robot : Robot
            Robot to add to the World
        """
        self._robots.add(robot)
        robot._add_to_world(self._grid_width, self._grid_height)

    def add_environment(self, img_filename: str):
        """
        Add an image to the environment for the Robots to sense. This will also
        be shown by the Viewer.

        Because sensing is cell-based, images will be scaled to the size of the
        World's grid. If the aspect ratio does not match, images will be
        stretched. To avoid any surprises from rescaling, we recommend using an
        image with the same resolution as your grid size. (e.g., if you have a
        50x50 grid, use a 50px x 50px image.)

        Parameters
        ----------
        img_filename : str
            Filename of the RGB image to use as a background environment. Any
            transparency (alpha) is ignored by the robot sensing.
        """
        # Add an image as an environment
        self.has_environment = True
        self._environment = WorldEnvironment(
            img_filename,
            (self._grid_width, self._grid_height))
        # Make sure all the Robots have the environment information
        [r._add_to_world(self._grid_width, self._grid_height, self._environment)
         for r in self._robots]

    def _communicate(self):
        """
        Run all pairwise communication of robots from broadcast messages.

        This checks that the receiving robots are of the right type (specified
        by the Mesage), and that robots are within mutual communication range of
        each other
        """
        # (Slow) loop through all robot pairs
        for tx_r in self._robots:  # transmitting robot
            msg = tx_r.get_tx_message()
            if not msg.is_null:  # only transmit non-empty messages
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
        Get the current time of the World. At the moment, that's just the number
        of ticks (time steps) since the simulation started, since we're in a
        discrete world.

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


class WorldEnvironment:
    """
    This represent the pattern in the world's environment, represented by an
    image.
    """

    def __init__(self, img_filename: str, grid_dim: Tuple[int, int]):
        """
        Use the provided image as the background for the world.

        Parameters
        ----------
        img_filename : str
            Filename + path of the image to use as the environment.
        grid_dim : Tuple[int, int]
            (width, height) of the World grid
        """
        self._img_filename = img_filename
        self.is_in_viewer = False

        # Get the scaling between image dimensions and grid world dimensions
        img = Image.open(img_filename).convert('RGB')
        self._world_dim = grid_dim
        self._world_img = img.resize(grid_dim, Image.NEAREST)
        self._world_img.show()

    def get(self, pos: Tuple[int, int]) -> Tuple[int, int, int]:
        """
        Get the RGB color in the given (x,y) cell

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position for which to get the color

        Returns
        -------
        Tuple[int, int, int]
            (red, blue, green) color of the environment in the given cell
        """
        # Get color in this grid cell
        color = self._world_img.getpixel(pos)
        return color

    def add_to_viewer(self, window_dim: Tuple[int, int]):
        """
        When a Viewer is created, this function is called to generate the pygame
        image for drawing

        Parameters
        ----------
        window_dim : Tuple[int, int]
            (width, height) of the Viewer window, in pixels (for image scaling)
        """
        # Add to the viewer for drawing
        self.is_in_viewer = True
        # Get the window scaling to create a scaled PyGame image to fit the
        # display window dimensions
        # img = pygame.image.load(self._img_filename).convert()
        raw_str = self._world_img.tobytes("raw", 'RGB')
        img = pygame.image.fromstring(raw_str, self._world_img.size, 'RGB')
        img = pygame.transform.scale(img, self._world_dim)
        self.viewer_img = pygame.transform.scale(img, window_dim)
