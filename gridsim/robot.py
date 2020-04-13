"""
Base class for all robot classes
"""

from abc import ABC, abstractmethod
import random

import pygame


class Robot(ABC):
    def __init__(self, x: int, y: int):
        self._id = random.getrandbits(32)  # Random 32-bit integer
        self._x = x
        self._y = y
        self._robot_init()

        # TODO: Not sure if this is the best way to handle the viewer sprite?
        self.sprite = pygame.sprite.Sprite()

    def _robot_init(self):
        # Run any robot-specific initialization
        # TODO: Any other initialization to do here?
        print('"_robot_initialization" not implemented (fully) yet')
        self.init()

    def sprite_setup(self, cell_size):
        # TODO: Setup sprite (called by viewer)
        print('"sprite_setup" not implemented (fully) yet')

        pass

    def move(self):
        # TODO: Move the robot (possibly dealing with collisions?)
        print('"Robot.move" not implemented yet')
        pass

    @abstractmethod
    def init(self):
        # Robot-specific initialization
        pass

    @abstractmethod
    def controller(self):
        # Robot specific controller run at each step
        pass

    @abstractmethod
    def comm_criteria(self) -> bool:
        # Criterion for whether message can be communicated
        pass

    @abstractmethod
    def receive_msg(self):
        # Robot processing a message that it receives
        pass
