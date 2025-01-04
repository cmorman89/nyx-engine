"""
Abstract Base System Module

This module defines the abstract base classes that all systems in the ECS architechture inherit
from.
"""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyx.nyx_engine.nyx_engine import NyxEngine


class BaseSystem(ABC):
    """The base system class, which all systems in the ECS architecture inherit from."""

    @property
    def engine(self) -> "NyxEngine":
        """Return the engine instance."""
        from nyx.nyx_engine.nyx_engine import NyxEngine

        return NyxEngine()
