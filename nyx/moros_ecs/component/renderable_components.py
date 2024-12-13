from abc import ABC

import numpy as np
from nyx.moros_ecs.component.nyx_component import NyxComponent


class RenderableComponent(NyxComponent, ABC):
    """Abstract base class of all components that can be rendered by HemeraTerm"""


class BackgroundColorComponent(RenderableComponent):
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


class ZIndexComponent(RenderableComponent):
    """Defines the layer prioritization (higher = higher priority)"""

    def __init__(self, z_index: int):
        self.z_index: int = z_index


class TilemapComponent(RenderableComponent):
    """Holds the 2D NumPy array of tile IDs that compose the tilemap and the size of a tile"""

    def __init__(self, tilemap: np.ndarray, tile_dimension: int = 16):
        if not isinstance(tilemap, np.ndarray) or tilemap.dtype != np.uint8:
            raise ValueError("Tilemap must be a NumPy `ndarray` of `dtype` 'uint8'")

        self.tilemap = tilemap
        self.tile_dimension = tile_dimension

    def __str__(self):
        """Return the class name (which is same as component name) when called as string."""
        return f"{type(self).__name__}"


class DimensionsComponent(RenderableComponent):
    def __init__(self, height: int, width: int):
        """Creates height, width bounds for an entity."""
        self.height = height
        self.width = width


class PositionComponenta(RenderableComponent):
    """Position of the the (0,0) origin of the entity within the frame."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
