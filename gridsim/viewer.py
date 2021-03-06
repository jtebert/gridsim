"""
The Viewer is a simple way to visualize your simulations. After creating the Viewer, just call
:meth:`~gridsim.viewer.Viewer.draw` each step (or less frequently) to see the current state of the
World.

.. note::
   The maximum Viewer refresh rate (set at creation with the ``display_rate`` argument) also limits
   the simulation rate. If you want to run faster/higher-throughput simulations, don't use the
   Viewer, or make it draw less frequently than every tick.
"""

import os
import math

import pygame
from PIL import Image

from .world import World


class Viewer:
    """Viewer to display the simulation of a World.

    This is optional (for debugging and visualization); simulations can be run much faster if
    the Viewer is not used.

    Parameters
    ----------
    world : World
        World to display
    window_width : int, optional
        Width (in pixels) of the window to display the World, by default 1080
    display_rate : int, optional
        How fast to update the view (ticks/s), by default 10. In each tick, robots will move by one
        cell, so keep this low to be able to interpret what's going on.
    show_grid : bool, optional
        Whether to show the underlying grid in the World, by default False.
    show_network : bool, optional
        Whether to visualize the current communication network of the robots, by default False.
        Communication connections between robots are shown as lines between robots.
    show_time : bool, optional
        Whether to draw the time (ticks) as text within the viewer window, by default False. (It is
        placed in the upper right corner.)
    """

    def __init__(self, world: World, window_width: int = 1080, display_rate: int = 10,
                 show_grid: bool = False, show_network: bool = False,
                 show_time: bool = False):

        self._world = world
        self._clock = pygame.time.Clock()
        self._tick_rate = display_rate
        self._show_grid = show_grid
        self._show_network = show_network
        self._show_time = show_time

        self._world_dim = world.get_dimensions()
        # Note: there is no guarantee that cell_size is an integer number of pixels
        self._cell_size = window_width / self._world_dim[0]
        self._window_dim = (window_width,
                            int(self._cell_size * self._world_dim[1]))

        if self._show_time:
            pygame.font.init()
            self._font = pygame.font.SysFont(None, 48)
        else:
            self._font = None

        # This allows setting an environment variable to avoid drawing stuff
        # when no display is set up (e.g., Travis CI)
        self._has_screen = bool(os.getenv('HAS_SCREEN', True))
        if self._has_screen:
            self._screen = pygame.display.set_mode(self._window_dim)

        # Set up all of the sprites for all of the robots
        [r._sprite_setup(self._cell_size) for r in self._world.get_robots()]

    def _update_bg(self):
        """
        Draw a background image for the Viewer (with the World's environment, possibly with a grid)
        onto the Screen.
        """
        if self._world.has_new_environment():
            self._world.get_environment().add_to_viewer(self._window_dim)
            bg = self._world.get_environment().get_viewer_img().copy()

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
            self._bg = bg

    def _draw_tagged_cells(self):
        # Draw the tagged cells onto the background
        tagged_pos = self._world._tagged_pos.copy()
        # Decrease opacity
        tagged_pos[:, :, 3] = tagged_pos[:, :, 3] * .25
        tag_dims = tagged_pos.shape
        pil_img = Image.fromarray(tagged_pos, mode='RGBA')
        # Convert to Pygame image
        raw_str = pil_img.tobytes('raw', 'RGBA')
        img = pygame.image.fromstring(raw_str, (tag_dims[1], tag_dims[0]), 'RGBA')
        # Resize to match the viewer window
        img = pygame.transform.scale(img, self._window_dim)
        # Draw it
        self._screen.blit(img, (0, 0))

    def _draw_network(self):
        """
        Generate a visualization of what robots are communicating with what other robots
        """
        robot_edge_inds = self._world._viewer_comm_edges
        for tx_r, rx_r, in robot_edge_inds:
            tx_pos = tx_r.rect.center
            rx_pos = rx_r.rect.center
            if tx_pos != rx_pos:
                pygame.draw.line(self._screen, (0, 0, 0), tx_pos, rx_pos)
            # pygame.gfxdraw.line(self._screen, rx_pos[0], rx_pos[1], tx_pos[0], tx_pos[1], (0, 0, 0))

    def draw(self):
        """
        Draw all of the robots in the World into the World and its environment.

        This will also draw the World's environment (if one is set) and any tagged cells in the
        World.
        """
        if self._has_screen:
            time_text = str(self._world.get_time())
            # Set the window title
            pygame.display.set_caption(
                f'Gridsim (t={time_text})')

            # If the world has a new environment, change the viewer background
            self._update_bg()
            # Clear everything by drawing the background
            self._screen.blit(self._bg, (0, 0))
            self._draw_tagged_cells()

            # Draw the communication network, if enabled
            if self._show_network:
                self._draw_network()

            # Draw the time, if set
            if self._show_time:
                time_surf = self._font.render(time_text, True, (0, 0, 0))
                self._screen.blit(time_surf, (self._window_dim[0]-128, 16))

            # Draw all the robots
            # Overrides sprite.Group.draw() method (see pygame source code)
            robots = self._world.get_robots()
            sprites = robots.sprites()
            # robots.draw(self._screen)
            for spr in sprites:
                if not spr.is_sprite_setup:
                    spr._sprite_setup(self._cell_size)
                robots.spritedict[spr] = self._screen.blit(spr.image, spr.rect)
            self.lostsprites = []

            # Update the display
            pygame.display.flip()
            self._clock.tick(self._tick_rate)
