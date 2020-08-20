from typing import Tuple, Optional
from pathlib import Path

import pygame
from PIL import Image


class Environment:
    """
    A null class representing both empty and non-empty Environments
    """

    def __init__(self):
        self.is_in_viewer = False
        # This is a placeholder empty image
        self._viewer_img = pygame.Surface((0, 0))

    def get(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int, int]]:
        """
        Get the RGB color in the given (x,y) cell. For a null environment, this always returns (0,
        0, 0) (black)

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position for which to get the color

        Returns
        -------
        Optional[Tuple[int, int, int]]:
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
        """
        if self.is_in_viewer:
            return self._viewer_img
        else:
            raise ValueError("Can't get the image because the environment" +
                             " hasn't been added to the viewer")


class ImageEnvironment(Environment):
    """
    This represent the pattern in the world's environment, represented by an image.
    """

    def __init__(self, img_filename: str, grid_dim: Tuple[int, int]):
        """
        Use the provided image as the background for the world.

        Parameters
        ----------
        img_filename : str
            Filename + path of the image to use as the environment.
        grid_dim : Tuple[int, int]
            (width, height) of the World grid
        """
        super().__init__()

        self._img_filename = Path(img_filename).expanduser().resolve()

        # Get the scaling between image dimensions and grid world dimensions
        img = Image.open(self._img_filename).convert('RGB')
        self._world_dim = grid_dim
        self._world_img = img.resize(grid_dim, Image.NEAREST)

    def __bool__(self):
        # All non-empty environments are True
        return True

    def get(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int, int]]:
        """
        Get the RGB color in the given (x,y) cell

        Parameters
        ----------
        pos : Tuple[int, int]
            (x, y) grid cell position for which to get the color

        Returns
        -------
        Optional[Tuple[int, int, int]]:
            (red, blue, green) color of the environment in the given cell. If the given position is
            outside of the arena/image, it will return None.
        """
        # Get color in this grid cell
        if (0 <= pos[0] < self._world_dim[0]) and (0 <= pos[1] < self._world_dim[1]):
            color = self._world_img.getpixel(pos)
            return color
        else:
            return None

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
        raw_str = self._world_img.tobytes("raw", 'RGB')
        img = pygame.image.fromstring(raw_str, self._world_img.size, 'RGB')
        img = pygame.transform.scale(img, self._world_dim)
        self._viewer_img = pygame.transform.scale(img, window_dim)
