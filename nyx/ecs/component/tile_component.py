from abc import ABC
import numpy as np


class NyxComponent(ABC):
    """Abstract base class of all components in NyxEngine."""


class TransformComponent(NyxComponent):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class GraphicComponent(NyxComponent):
    def __init__(self, graphic: np.ndarray):
        if not isinstance(graphic, np.ndarray) or graphic.dtype != np.uint8:
            raise ValueError("Graphic must be a numpy ndarray of dtype 'uint8'")
        self.graphic = graphic


class TileMapComponent(NyxComponent):
    def __init__(self, tilemap: np.ndarray, tile_width: int = 1, tile_height: int = 1):
        if not isinstance(tilemap, np.ndarray) or tilemap.dtype != np.uint8:
            raise ValueError("Tilemap must be a NumPy `ndarray` of `dtype` 'uint8'")

        self.tilemap = tilemap
        self.tile_width = tile_width
        self.tile_height - tile_height
