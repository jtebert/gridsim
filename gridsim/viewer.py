"""
[Optional] For viewing the simulations, using Pygame
"""

import pygame

from .world import World


class Viewer:
    def __init__(self, world: World, window_width: int = 1080,
                 display_rate: int = 10, show_grid: bool = True):
        """
        Create a Viewer to display the simulation of a World.

        This is optional (for debugging and visualization); simulations can be
        run much faster if the Viewer is not used.

        Parameters
        ----------
        world : World
            World to display
        window_width : int, optional
            Width (in pixels) of the window to display the World, by default
            1080
        display_rate : int, optional
            How fast to update the view (ticks/s), by default 10. In each tick,
            robots will move by one cell, so keep this low to be able to
            interpret what's going on.
        show_grid : bool, optional
            Whether to show the underlying grid in the World, by default True.
            If false, it's blank.
        """
        self._world = world
        self._clock = pygame.time.Clock()
        self._tick_rate = display_rate

        world_dim = world.get_dimensions()
        self._cell_size = window_width / world_dim[0]
        self._window_dim = (window_width, int(self._cell_size * world_dim[1]))

        self._screen = pygame.display.set_mode(self._window_dim)

        # Set up all of the sprites for all of the robots
        [r._sprite_setup(self._cell_size) for r in self._world.get_robots()]

        # Set up background grid
        self._bg = pygame.Surface(self._window_dim)
        self._bg.fill((20, 20, 20))
        if show_grid:
            for col in range(1, world_dim[0]):
                x = col * self._cell_size
                pygame.draw.lines(self._bg, (50, 50, 50), False,
                                  [(x, 0),
                                   (x, self._window_dim[1])],
                                  1)
            for row in range(1, world_dim[1]):
                y = row * self._cell_size
                pygame.draw.lines(self._bg, (50, 50, 50,), False,
                                  [(0, y),
                                   (self._window_dim[0], y)],
                                  1)

    def draw(self):
        """
        Draw all of the robots in the world onto the background.
        """
        self._screen.blit(self._bg, (0, 0))

        # Draw all the robots
        # Overrides sprite.Group.draw() method (see pygame source code)
        robots = self._world.get_robots()
        sprites = robots.sprites()
        surface_blit = self._screen.blit
        for spr in sprites:
            if not spr.is_sprite_setup:
                spr._sprite_setup(self._cell_size)
            robots.spritedict[spr] = \
                surface_blit(spr.image, spr.rect)
        self.lostsprites = []

        # Update the display
        pygame.display.flip()
        self._clock.tick(self._tick_rate)
