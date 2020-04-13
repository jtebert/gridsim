"""
[Optional] For viewing the simulations, using Pygame
"""

import pygame

from .world import World


class Viewer:
    def __init__(self, world: World, window_width: int = 1080):
        self._world = world

        world_dim = world.get_dimensions()
        cell_px = window_width / world_dim[0]
        self._window_dim = (window_width,  int(cell_px * world_dim[1]))

        self._screen = pygame.display.set_mode(self._window_dim)

        # Set up all of the sprites for all of the robots
        [r.sprite_setup(cell_px) for r in self._world._robots]

    def draw(self):
        # TODO: Draw the world (all the robots, possibly the base station?)
        print('"Viewer.draw" not implemented yet')
        self._screen.fill((0, 0, 0))

        for robot in self._world._robots:
            pass

        # self._screen.blit(ball, ballrect)
        pygame.display.flip()
