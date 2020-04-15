"""
Simulate the grid-based world, full of robots
"""

from typing import Tuple, List

import pygame

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
        [r.add_to_world(self._grid_width, self._grid_height) for r in robots]
        self._robots = pygame.sprite.Group(robots)
        self._allow_collisions = allow_collisions
        self._tick = 0

    def step(self):
        """
        Run a single step of the simulation. This moves the robots, manages the
        clock, and runs the robot controllers.
        """
        # One tick of the world
        # self._run_controllers()
        # self._communicate()
        # self._move()
        self._robots.update()
        self._communicate()
        self._tick += 1

    def add_robot(self, robot: Robot):
        """
        Add a single robot to the World

        Parameters
        ----------
        robot : Robot
            Robot to add to the World
        """
        self._robots.add(robot)
        robot.add_to_world(self._grid_width, self._grid_height)

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

    # def _run_controllers(self):
    #     # Run the robot controllers
    #     [robot.controller() for robot in self._robots]

    # def _move(self):
    #     # TODO: Move all of the robots (requires checking for edges and
    #     # (possibly) collisions)
    #     print('"_move" not implemented yet')
    #     pass

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
