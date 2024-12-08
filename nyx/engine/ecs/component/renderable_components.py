from abc import ABC
from nyx.engine.ecs.component.nyx_component import NyxComponent


class RenderableComponent(NyxComponent, ABC):
    """Abstract base class of all components that can be rendered by HemeraTerm"""


class BackgroundColorComponent(RenderableComponent):
    """Define a single ANSI color code (0-255)"""

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


# class TransformComponent(NyxComponent):
#     def __init__(self, x: int, y: int):
#         self.x = x
#         self.y = y


# class GraphicComponent(NyxComponent):
#     """Hold the 2D NumPy array/texture for sprites or other objects with behaviors."""

#     def __init__(self, graphic_arr: np.ndarray):
#         if not isinstance(graphic_arr, np.ndarray) or graphic_arr.dtype != np.uint8:
#             raise ValueError("Graphic must be a numpy ndarray of dtype 'uint8'")
#         self.graphic_arr = graphic_arr


# class TilemapComponent(NyxComponent):
#     """Holds the 2D NumPy array of tile IDs"""

#     def __init__(self, tilemap: np.ndarray, tilemap_bg: int = None):
#         if not isinstance(tilemap, np.ndarray) or tilemap.dtype != np.uint8:
#             raise ValueError("Tilemap must be a NumPy `ndarray` of `dtype` 'uint8'")

#         self.tilemap_arr = tilemap
#         self.tilemap_bg: int = tilemap_bg

#     def __str__(self):
#         """Return the class name (which is same as component name) when called as string."""
#         return f"{Type[self]}"
