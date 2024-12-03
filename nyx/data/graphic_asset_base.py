"""
Abstract Base Data Classes Module

This module houses the abstract classes for the data layer of NyxEngine.
"""

from abc import ABC


class GraphicAsset(ABC):
    """The root of the graphical asset component tree. Any object with a visual data component must
    inherit from this class.
    """

    pass


class RawGraphicAsset(GraphicAsset, ABC):
    """Represents any class holding a non-Nyx graphical object, such as a JSON dictionary or a PNG."""

    pass


class ProcessedGraphicAsset(GraphicAsset, ABC):
    """Represents any class holding a Nyx graphical object that can be used directly without
    requiring pre-processing."""

    pass
