from __future__ import annotations  # For the type checking circular import

from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING
import random
import numpy as np

import pygame

# from .message import Message
if TYPE_CHECKING:
    from .message import Message


class Robot(ABC, pygame.sprite.Sprite):
    """
    Base class for all robot classes
    """

    def __init__(self, x: int, y: int):
        """
        Abstract robot base class for all Robots

        Parameters
        ----------
        x : int
            Starting x position (grid cell) of the robot
        y : int
            Starting y position (grid cell) of the robot
        """
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer

        self.id = random.getrandbits(32)  # Random 32-bit integer
        self._x = x
        self._y = y
        self._cell_size = 0  # set in sprite_setup (when added to world)
        self._color = (255, 255, 255)
        self._move_cmd = (0, 0)
        self._arena_dim = (0, 0)
        self.tick = 0
        from .message import Message  # Here to fix circular import
        self._tx_message = Message()  # Start with a null/blank message

        self.is_sprite_setup = False

        # Robot-specific initialization
        self.init()

    def add_to_world(self, arena_width: int, arena_height: int):
        """
        Add a robot to the world by telling it the world's dimensions

        Parameters
        ----------
        arena_width : int
            Grid width of the arena
        arena_height : int
            Grid height of the arena
        """
        # Tell the robot the size of the world
        # TODO: In future gets the light pattern as well
        self._arena_dim = (arena_width, arena_height)

    def sprite_setup(self, cell_size):
        # TODO: Setup sprite (called by viewer) for add_to_world
        self._cell_size = cell_size
        self.image = pygame.Surface([cell_size, cell_size], pygame.SRCALPHA)
        r = int(cell_size/2)
        pygame.draw.circle(self.image, self._color,
                           (r, r), int(r*.9))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self._x*cell_size, self._y*cell_size)
        self.is_sprite_setup = True

    def update(self):
        """
        Run the robot's controller, move the robot, and (if Viewer is being
        used), update the Sprite information.

        (The update() function comes from the Sprite class.)
        """
        self._controller()
        self._move()
        # Reset movement command between steps
        self._move_cmd = (0, 0)

        self.tick += 1

        # Update position for viewer
        if self.is_sprite_setup:
            self.rect.topleft = (self._x*self._cell_size,
                                 self._y*self._cell_size)
            pygame.draw.circle(
                self.image, self._color,
                (int(self._cell_size/2), int(self._cell_size/2)),  # x, y pos
                int(self._cell_size/2*.9))  # radius

    def move(self, x: int, y: int):
        """
        User-facing move command, essentially sending a request to move in a
        certain direction/amount. The robot will only make this move if it
        doesn't violate any movement conditions (such as edge of arena or, if
        enabled, collisions with other robots)

        Parameters
        ----------
        x : int
            Number of grid cells to move in x direction, relative to current
            position
        y : int
            Number of grid cells to move in y direction, relative to current
            position
        """
        # Move by x, y cells
        self._move_cmd = (x, y)

    def _move(self):
        """
        Actually (possibly) move the robot, subject to constraints. Robot will
        only be moved if it will stay in the arena.

        Right now there is no collision checking.
        """
        # TODO: Move the robot (possibly dealing with collisions?)
        tmp_pos = (self._x + self._move_cmd[0], self._y + self._move_cmd[1])
        # Only move if you'll stay in the arena
        # Currently this ignores between-robot collisions
        if tmp_pos[0] < self._arena_dim[0] and \
           tmp_pos[1] < self._arena_dim[1] and \
           tmp_pos[0] >= 0 and tmp_pos[1] >= 0:
            self._x = tmp_pos[0]
            self._y = tmp_pos[1]

    def set_color(self, r: int, g: int, b: int):
        """
        Set the color of the robot (as shown in Viewer) with 8-bit RGB values

        Parameters
        ----------
        r : int
            Red channel [0, 255]
        g : int
            Green channel [0, 255]
        b : int
            Blue channel [0, 255]

        Raises
        ------
        ValueError
            If all values are not in the range [0, 255]
        """
        # Set the RGB color (0-255 for RGB channels)
        color = (r, g, b)
        if all([0 <= c <= 255 for c in color]):
            self._color = color
        else:
            raise ValueError('RGB values must all be in the range [0, 255]')

    def get_pos(self) -> Tuple[int, int]:
        """
        Get the position of the robot in the grid

        Returns
        -------
        Tuple[int, int]
            (x, y) grid position of the robot, from the top left
        """
        return self._x, self._y

    def get_tx_message(self) -> Message:
        """
        Get the message queued for transmission (broadcast).

        The message is set by the `set_tx_message` function

        Returns
        -------
        Message
            Message to continuously broadcast
        """
        return self._tx_message

    def set_tx_message(self, msg: Message):
        """
        Set the message that will be continuously broadcast

        Parameters
        ----------
        msg : Message
            Message to send to anyone within range
        """
        self._tx_message = msg

    def _controller(self):
        # Robot specific controller run at each step
        self.loop()

    def distance(self, pos: Tuple[int, int]) -> float:
        """
        Get the Euclidean distance (in grid cells) between this robot and the
        specified (x, y) grid cell position.

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell coordinate to get the distance to

        Returns
        -------
        float
            Euclidean distance of this robot from the given coordinate
        """
        # TODO: Move to abstract/subclass to allow customized distance metric?
        # return np.abs(self._x - pos[0]) + np.abs(self._y - pos[1])# Manhattan
        return np.sqrt((self._x - pos[0])**2+(self._y-pos[1])**2)

    @abstractmethod
    def init(self):
        """
        Robot-specific initialization that will be run when the robot is set up
        """
        pass

    @abstractmethod
    def loop(self):
        """
        User-implemented loop operation (code the robot runs every loop)
        """
        pass

    @abstractmethod
    def comm_criteria(self, dist: int) -> bool:
        """
        Criterion for whether message can be communicated (base on distance)

        Parameters
        ----------
        dist : int
            Distance between this robot and the other robot

        Returns
        -------
        bool
            Whether or not the other robot is within communication range
        """
        pass

    @abstractmethod
    def receive_msg(self, msg: Message, dist: float):
        """
        Function called when the robot receives a message. This allows the
        specific robot implementation to choose how to process the messages that
        it receives, asynchronously.

        Parameters
        ----------
        msg : Message
            Received message from another robot
        dist : float
            Distance of the sending robot from this robot
        """
        pass

    # @abstractmethod
    # def msg_received(self):
    #     # Called when a robot successfully sent its message
    #     pass
