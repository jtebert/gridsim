"""
Simulate the grid-based world, full of robots
"""

from typing import Optional, List
from .robot import Robot


class World:

    def __init__(self, width: int, height: int,
                 robots: Optional[List[Robot]] = [],
                 allow_collisions: bool = True):
        self._grid_width = width
        self._grid_height = height
        self._robots = robots
        self._tick = 0
        self._allow_collisions = allow_collisions

    def step(self):
        # One tick of the world
        self._run_controllers()
        self._communicate()
        self._move()
        self._tick = self._tick + 1

    def add_robot(self):
        # TODO: Add a single robot to the world
        print('"add_robot" not implemented yet')
        pass

    def _run_controllers(self):
        # Run the robot controllers
        [robot.controller() for robot in self._robots()]

    def _communicate(self):
        # TODO: Do all pairwise communication between robots
        print('"_communicate" not implemented yet')
        pass

    def _move(self):
        # TODO: Move all of the robots (requires checking for edges and
        # (possibly) collisions)
        print('"_move" not implemented yet')
        pass
