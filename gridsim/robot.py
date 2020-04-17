from __future__ import annotations  # For the type checking circular import

from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING, Optional
import random
import numpy as np

import pygame

# from .message import Message
if TYPE_CHECKING:
    from .message import Message
    from .world import WorldEnvironment


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

        #: Unique ID of the Robot
        self.id: int = random.getrandbits(32)  # Random 32-bit integer
        self._x = x
        self._y = y
        self._cell_size = 0.  # set in sprite_setup (when added to world)
        self._color = (255, 255, 255)
        self._arena_dim = (0, 0)
        self._tick = 0
        from .message import Message  # Here to fix circular import
        self._tx_message = Message()  # Start with a null/blank message

        self._is_in_world = False
        self.is_sprite_setup = False

        # Set by add_to_world, if world has an environment
        self._environment: Optional[WorldEnvironment] = None

        # Robot-specific initialization
        self.init()

    def _add_to_world(self, arena_width: int, arena_height: int,
                      environment: Optional[WorldEnvironment] = None):
        """
        Add a robot to the world by telling it the world's dimensions

        Parameters
        ----------
        arena_width : int
            Grid width of the arena
        arena_height : int
            Grid height of the arena
        environment: WorldEnvironment
            Representation of the world as an image (for sampling color)
        """
        # Tell the robot the size of the world
        # TODO: In future gets the light pattern as well
        self._arena_dim = (arena_width, arena_height)
        self._is_in_world = True

        # Add the World's environment, if it has one
        self._environment = environment

    def sample(self, pos: Optional[Tuple[int, int]] = None) -> \
            Tuple[int, int, int]:
        """
        Sample the RGB environment at the given cell location, or (if no ``pos``
        given) and the robot's current position.

        This allows you to sample *any* location in the World, but this is
        **probably cheating**. The robot platform you're modeling likely doesn't
        have such extensive sensing capabilities. This function is provided so
        that you can define any custom sensing capabilities (such as within a
        radius around your robot, or a line of sight sensor).

        Parameters
        ----------
        pos : Optional[Tuple[int, int]]
            (x, y) grid cell position of the World to sample. If not specified,
            the current robot position is sampled.

        Returns
        -------
        Tuple
            (red, green, blue) color at the given coordinate in the range
            [0, 255]. If the world does not have an environment set, this will
            return (0, 0, 0)
        """
        if self._environment is not None:
            if pos is None:
                return self._environment.get(self.get_pos())
            else:
                return self._environment.get(pos)
        else:
            return 0, 0, 0

    def _sprite_setup(self, cell_size: float):
        """
        Set up the Sprite image/rectangle, called if a Viewer is being used.

        Parameters
        ----------
        cell_size : float
            Side length of square cells in pixels, for determining size to draw
            the Robot.
        """
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

        # Update position/color for viewer
        if self.is_sprite_setup:
            self.rect.topleft = (self._x*self._cell_size,
                                 self._y*self._cell_size)

        # Call the platform-specific movement operation
        new_pos = self.move()
        # Run the robot's loop function
        self._controller()
        # Actually change the robot's position (or don't) based on collisions
        self._move(new_pos)

        self._tick += 1

    def _move(self, new_pos: Tuple[int, int]):
        """
        Actually (possibly) move the robot, subject to constraints. Robot will
        only be moved if it will stay in the arena.

        Right now there is no collision checking.
        """
        # TODO: Move the robot (possibly dealing with collisions?)
        # Only move if you'll stay in the arena
        # Currently this ignores between-robot collisions
        if new_pos[0] < self._arena_dim[0] and \
           new_pos[1] < self._arena_dim[1] and \
           new_pos[0] >= 0 and new_pos[1] >= 0:
            self._x = new_pos[0]
            self._y = new_pos[1]

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

        if self.is_sprite_setup:
            pygame.draw.circle(
                self.image, self._color,
                (int(self._cell_size/2), int(self._cell_size/2)),  # x, y pos
                int(self._cell_size/2*.9))  # radius

    def get_pos(self) -> Tuple[int, int]:
        """
        Get the position of the robot in the grid

        Returns
        -------
        Tuple[int, int]
            (x, y) grid position of the robot, from the top left
        """
        return self._x, self._y

    def get_tick(self) -> int:
        """
        Get the current tick of the robot (how many steps since the simulation
        started).

        Returns
        -------
        int
            Number of ticks since start of simulation
        """
        return self._tick

    def get_world_dim(self) -> Tuple[int, int]:
        """
        Get the dimensions of the World that this Robot is in, so it can plan to
        avoid hitting the boundaries.

        Returns
        -------
        Tuple[int, int]
            (width, height) dimensions of the world, in grid cells

        Raises
        ------
        ValueError
            Cannot get dimensions if Robot is not in a World. Add it during
            creation of a World or with :meth:`~gridsim.world.World.add_robot`.
        """
        if self._is_in_world:
            return self._arena_dim
        else:
            raise ValueError("Cannot get dimensions because " +
                             "Robot is not in a World.")

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
        # TODO: Possibly add battery life here
        self.loop()

    def distance(self, pos: Tuple[int, int]) -> float:
        """
        Get the Euclidean distance (in grid cells) between this robot and the
        specified (x, y) grid cell position.

        If you want to change the distance metric (e.g., use Manhattan distance
        instead), you can override this method when you extend the Robot class.

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
    def move(self) -> Tuple[int, int]:
        """
        User-facing move command, essentially sending a request to move to a
        particular cell.

        The robot will only make this move if it doesn't violate any movement
        conditions (such as edge of arena or, if enabled, collisions with other
        robots). Therefore, you do NOT need to implement any collision or
        edge-of-arena detection in this function.

        Returns
        -------
        Tuple[int, int]
            (x, y) grid cell position the robot intends to move to
        """
        pass

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

    def msg_received(self):
        """
        This is called when a robot successfully sent its message (i.e., when
        another robot received its message.)

        By default, this does nothing. You can override it in your robot class
        to execute some operation or set a flag when a message is sent.
        """
        pass
