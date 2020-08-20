from typing import Tuple

from .robot import Robot
# If you are building your own Robot class, you would instead use:
# from gridsim import Robot


class GridRobot(Robot):
    STAY = 'stay'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    DIRS = [STAY, UP, DOWN, LEFT, RIGHT]

    def __init__(self, x: int, y: int, comm_range: float = 5):
        """
        Create a robot that moves along the cardinal directions. Optionally, you can specify a
        communication range for the robots.

        Parameters
        ----------
        x : int
            Starting x position (grid cell) of the robot
        y : int
            Starting y position (grid cell) of the robot
        comm_range : float, optional
            Communication radius (in grid cells) of the robot, by default 5
        """
        # Run all of the initialization for the default Robot class, including
        # setting the starting position
        super().__init__(x, y)

        self._comm_range = comm_range
        # Start with the robot stationary
        self._move_cmd = GridRobot.STAY

    def set_direction(self, dir: str):
        """
        Helper function to set the direction the robot will move. Note that this will persist (the
        robot will keep moving) until the direction is changed.

        Parameters
        ----------
        dir : int
            Direction to move, one of ``GridRobot.UP``, ``GridRobot.DOWN``, ``GridRobot.LEFT``,
            ``GridRobot.RIGHT``, or ``GridRobot.STAY``

        Raises
        ------
        ValueError
            If given direction is not one of `GridRobot.UP``, ``GridRobot.DOWN``,
            ``GridRobot.LEFT``, ``GridRobot.RIGHT``, or ``GridRobot.STAY``
        """
        if dir in GridRobot.DIRS:
            self._move_cmd = dir
        else:
            raise ValueError('Invalid movement direction "{}"'.format(dir))

    def move(self) -> Tuple[int, int]:
        """
        Determine the cell the Robot will move to, based on the direction set in by
        :meth:`~gridsim.grid_robot.GridRobot.set_motors`.

        Returns
        -------
        Tuple[int, int]
            (x,y) grid cell the robot will move to, if possible/allowed
        """
        x, y = self.get_pos()
        if self._move_cmd == GridRobot.UP:
            y -= 1
        elif self._move_cmd == GridRobot.DOWN:
            y += 1
        elif self._move_cmd == GridRobot.RIGHT:
            x += 1
        elif self._move_cmd == GridRobot.LEFT:
            x -= 1
        # else STAY, which keeps current position
        return x, y

    def comm_criteria(self, dist: int) -> bool:
        """
        Robots can communicate if their Euclidean distance is <= the radius specified at
        initialization (by default, 5 cells)

        Parameters
        ----------
        dist : int
            Euclidean distance of the other robot with which to communicate

        Returns
        -------
        bool
            Whether distance is <= the communication radius
        """
        return dist <= self._comm_range
