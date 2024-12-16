"""
Scene Components Module

This module contains scene-level components that can be rendered by Aether, such as a background
color and a tilemap.
"""

import numpy as np
from nyx.moirai_ecs.component.base_components import NyxComponent


class SceneComponent(NyxComponent):
    """Signify entity as a high level/top level component"""

    def __init__(self, friendly_name: str):
        self.friendly_name = friendly_name


class BackgroundColorComponent(NyxComponent):
    """Defines a single ANSI color code (0-255)"""

    def __init__(self, bg_color_code: int = 0):
        if 0 <= bg_color_code <= 255:
            self.bg_color_code = bg_color_code
        else:
            raise ValueError(
                f"Background color (={bg_color_code}) must be an int between 0 and 255."
            )

    def __repr__(self):
        return f"{type(self).__name__}(bg_color_code={self.bg_color_code})"


class TilemapComponent(NyxComponent):
    """Holds the 2D NumPy array of tile IDs that compose the tilemap and the size of a tile"""

    def __init__(self, tilemap: np.ndarray, tile_dimension: int = 16):
        if not isinstance(tilemap, np.ndarray) or tilemap.dtype != np.uint8:
            raise ValueError("Tilemap must be a NumPy `ndarray` of `dtype` 'uint8'")

        self.tilemap = tilemap
        self.tile_dimension = tile_dimension

    def __str__(self):
        """Return the class name (which is same as component name) when called as string."""
        return f"{type(self).__name__}"
