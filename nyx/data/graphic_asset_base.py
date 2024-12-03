"""
Abstract Base Data Classes Module

This module houses the abstract classes for the data layer of NyxEngine.
"""

from abc import ABC, abstractmethod


class GraphicAsset(ABC):
    """The root of the graphical asset component tree. Any object with a visual data component must
    inherit from this class.
    """

    @property
    @abstractmethod
    def payload(self):
        """Return data held by the graphic object.

        Must be implemented by subclass."""

    @payload.setter
    @abstractmethod
    def payload(self, payload):
        """Set data held by the graphic object.

        Must be implemented by subclass.

        Args:
            payload:The graphical data held by this object.
        """

    @abstractmethod
    def get_nyx_format(self):
        """Convert payload to Nyx format (NumPy-based) and return, or return the Nyx-formatted
        object if the payload is already Nyx format.

        Must be implemented by subclass."""

    @abstractmethod
    def get_png_format(self):
        """Convert the payload to a PNG image (if needed) and return it.

        Must be implemented by subclass."""

    @abstractmethod
    def get_json_format(self):
        """Convert the payload to a JSON dictionary (if needed) and return it.

        Must be implemented by subclass."""


class GraphicCollectionAsset(GraphicAsset, ABC):
    @property
    @abstractmethod
    def children(self):
        """Return the child assets held in this collection.

        Must be implemented by subclass.
        """

    @abstractmethod
    def add_child_asset(self, asset: GraphicAsset):
        """Add a new asset to this collections list of assets.

        Must be implemented by subclass.
        """

    @abstractmethod
    def remove_child_asset(self, asset_identifier: GraphicAsset | int):
        pass


class RawGraphicAsset(GraphicAsset, ABC):
    """Represents any class holding a non-Nyx graphical object, such as a JSON dictionary or a PNG."""

    pass


class ProcessedGraphicAsset(GraphicAsset, ABC):
    """Represents any class holding a Nyx graphical object that can be used directly without
    requiring pre-processing."""

    @abstractmethod
    def expand_n_array(self):
        pass
