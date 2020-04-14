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
        self._grid_width = width
        self._grid_height = height
        [r.add_to_world(self._grid_width, self._grid_height) for r in robots]
        self._robots = pygame.sprite.Group(robots)
        self._allow_collisions = allow_collisions
        self._tick = 0

    def step(self):
        # One tick of the world
        # self._run_controllers()
        # self._communicate()
        # self._move()
        self._robots.update()
        self._communicate()
        self._tick += 1

    def add_robot(self, robot: Robot):
        # Add a single robot to the world
        # robot.add_to_world()
        self._robots.add(robot)

    def _communicate(self):
        # TODO: Do all pairwise communication between robots

        # (Slow) loop through all robot pairs
        for tx_r in self._robots:  # transmitting robot
            msg = tx_r.get_tx_message()
            if not msg.is_null:  # only transmit non-empty messages
                for rx_r in self._robots:  # receiving robot
                    # Receiver must be target type (and not itself)
                    if tx_r != rx_r and isinstance(msg._receiver_type, rx_r):
                        dist = tx_r.distance(rx_r.get_pos())
                        if tx_r.comm_criteria(dist) and \
                                rx_r.comm_criteria(dist):
                            # Receiving robot processes incoming message
                            rx_r.receive_msg(msg, dist)
                            # Tell sender that the message sent successfully
                            tx_r.received()

    # def _run_controllers(self):
    #     # Run the robot controllers
    #     [robot.controller() for robot in self._robots]

    # def _move(self):
    #     # TODO: Move all of the robots (requires checking for edges and
    #     # (possibly) collisions)
    #     print('"_move" not implemented yet')
    #     pass

    def get_dimensions(self) -> Tuple[int, int]:
        return self._grid_width, self._grid_height
