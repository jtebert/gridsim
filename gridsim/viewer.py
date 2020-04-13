"""
[Optional] For viewing the simulations, using Pygame
"""

from .world import World


class Viewer:
    def __init__(self, world: World, window_width: int = 1080):
        self._world = world

    def draw(self):
        # TODO: Draw the world (all the robots, possibly the base station?)
        print('"Viewer.draw" not implemented yet')
        pass
