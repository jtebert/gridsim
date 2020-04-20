"""
[Optional] For viewing the simulations, using Pygame
"""

import pygame

from .world import World


class Viewer:
    def __init__(self, world: World, window_width: int = 1080,
                 display_rate: int = 10, show_grid: bool = False):
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
            Whether to show the underlying grid in the World, by default False.
        """
        self._world = world
        self._clock = pygame.time.Clock()
        self._tick_rate = display_rate
        self._show_grid = show_grid

        self._world_dim = world.get_dimensions()
        self._cell_size = window_width / self._world_dim[0]
        self._window_dim = (window_width, int(self._cell_size * self._world_dim[1]))

        self._screen = pygame.display.set_mode(self._window_dim)

        # Set up all of the sprites for all of the robots
        [r._sprite_setup(self._cell_size) for r in self._world.get_robots()]

        self._bg = self._create_bg()

    def _has_new_environment(self) -> bool:
        """
        Check of the World's environment has changed.

        Returns
        -------
        bool
            Whether the World's environment has changed (or one has been added)
        """
        return self._world.has_environment and \
            not self._world._environment.is_in_viewer

    def _create_bg(self) -> pygame.Surface:
        """
        Create a background image for the Viewer, with the World's environment
        (if it has one) and possibly with a grid

        Returns
        -------
        pygame.Surface
            Pygame image (surface) to use as a the Viewer background
        """
        if self._has_new_environment:
            self._world._environment.add_to_viewer(self._window_dim)
            bg_img = self._world._environment.viewer_img
        else:
            bg_img = None

        # Use background image or solid color
        if bg_img is None:
            bg = pygame.Surface(self._window_dim)
            bg.fill((20, 20, 20))
        else:
            bg = bg_img

        # Set up background grid
        if self._show_grid:
            for col in range(1, self._world_dim[0]):
                x = col * self._cell_size
                pygame.draw.lines(bg, (50, 50, 50), False,
                                  [(x, 0),
                                   (x, self._window_dim[1])],
                                  1)
            for row in range(1, self._world_dim[1]):
                y = row * self._cell_size
                pygame.draw.lines(bg, (50, 50, 50,), False,
                                  [(0, y),
                                   (self._window_dim[0], y)],
                                  1)
        return bg

    def draw(self):
        """
        Draw all of the robots in the world into the World and its environment.
        """
        # Set the window title
        pygame.display.set_caption(
            'Gridsim (t={})'.format(self._world.get_time()))

        # If the world has a new environment, change the viewer background
        if self._has_new_environment:
            self._bg = self._create_bg()
        # Clear everything by drawing the background
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
