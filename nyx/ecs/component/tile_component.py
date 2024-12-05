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
