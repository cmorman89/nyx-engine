"""
Abstract Base Component Module

This module defines the abstract base classes that all components in the ECS architechture inherit
from.
"""

from abc import ABC


class BaseComponent(ABC):
    """Abstract base class of all components in NyxEngine."""


class NyxComponent(BaseComponent, ABC):
    """Abstract base class of all components that can be rendered by HemeraTerm"""
