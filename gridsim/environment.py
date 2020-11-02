from typing import Tuple, Optional
from pathlib import Path

import pygame
from PIL import Image
import numpy as np


class Environment:
    """
    A null class representing both empty and non-empty Environments
    """

    def __init__(self):
        self.is_in_viewer = False
        # This is a placeholder empty image
        self._viewer_img = pygame.Surface((0, 0))

    def get(self, pos: Tuple[int, int]) -> Optional[Tuple[float, float, float]]:
        """
        Get the RGB color in the given (x,y) cell. For a null environment, this always returns (0,
        0, 0) (black)

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position for which to get the color

        Returns
        -------
        Tuple[float, float, float] or None:
            (0, 0, 0,) -- Null environment's color is always considered black.
        """
        return 0, 0, 0

    def add_to_viewer(self, window_dim: Tuple[int, int]):
        """
        When a Viewer is created, this function is called to generate the pygame image for drawing.

        FOR A NULL ENVIRONMENT, a black(ish) image is generated

        Parameters
        ----------
        window_dim : Tuple[int, int]
            (width, height) of the Viewer window, in pixels (for image scaling)
        """
        self.is_in_viewer = True
        self._viewer_img = pygame.Surface(window_dim)
        self._viewer_img.fill((20, 20, 20))

    def __bool__(self):
        # This is False because it's an empty environment
        return False

    def get_viewer_img(self) -> pygame.Surface:
        """
        Get the representation of the Environment in a form that the Viewer can draw (pygame image)

        Returns
        -------
        pygame.Surface
            Image of the Environment (background image)

        Raises
        ------
        ValueError
            If image is not in in the Viewer
        """
        if self.is_in_viewer:
            return self._viewer_img
        else:
            raise ValueError("Can't get the image because the environment"
                             " hasn't been added to the viewer")


class ImageEnvironment(Environment):
    """
    This represent the pattern in the world's environment with an Image

    Parameters
    ----------
    img_filename : str
        Filename + path of the image to use as the environment.
    grid_dim : Tuple[int, int]
        (width, height) of the World grid
    observation_stdev : float, optional
        If 0 (this is the default), observations will return the exact RGB value of environment
        image in each cell. If non-zero (should be >= 0), each component of the observations will be
        drawn from a normal distribution with mean at the image value, and using this standard
        deviation.
    """

    def __init__(self, img_filename: str, grid_dim: Tuple[int, int], observation_std: float = 0.):
        super().__init__()

        self._img_filename = Path(img_filename).expanduser().resolve()

        # Get the scaling between image dimensions and grid world dimensions
        img = Image.open(self._img_filename).convert('RGB')
        self._world_dim = grid_dim
        if img.size == grid_dim:
            self._world_img = img
        else:
            self._world_img = img.resize(grid_dim, Image.LANCZOS)

        self._observation_std = observation_std

    def __bool__(self):
        # All non-empty environments are True
        return True

    def get(self, pos: Tuple[int, int]) -> Optional[Tuple[float, float, float]]:
        """
        Get the RGB color in the given (x,y) cell

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position for which to get the color

        Returns
        -------
        Tuple[float, float, float] or None:
            (red, blue, green) color of the environment in the given cell. If the given position is
            outside of the arena/image, it will return None.
        """
        # Get color in this grid cell
        if (0 <= pos[0] < self._world_dim[0]) and (0 <= pos[1] < self._world_dim[1]):
            color = self._world_img.getpixel(pos)
        else:
            return None
        if self._observation_std != 0:
            return tuple(np.random.normal(c, self._observation_std) for c in color)
        else:
            return color

    def add_to_viewer(self, window_dim: Tuple[int, int]):
        """
        When a Viewer is created, this function is called to generate the pygame image for drawing

        Parameters
        ----------
        window_dim : Tuple[int, int]
            (width, height) of the Viewer window, in pixels (for image scaling)
        """
        # Add to the viewer for drawing
        self.is_in_viewer = True
        # Get the window scaling to create a scaled PyGame image to fit the
        # display window dimensions
        # img = pygame.image.load(self._img_filename).convert()

        # PIL image (1 px = 1 world cell) -> raw bytes
        raw_str = self._world_img.tobytes("raw", 'RGB')
        # raw bytes -> Pygame image
        img = pygame.image.fromstring(raw_str, self._world_img.size, 'RGB')
        # img = pygame.transform.scale(img, self._world_dim)
        # Scale pygame image to world viewer window dimensions
        self._viewer_img = pygame.transform.scale(img, window_dim)
