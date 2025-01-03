"""
Abstract Base System Module

This module defines the abstract base classes that all systems in the ECS architechture inherit
from.
"""

from abc import ABC


class BaseSystem(ABC):
    """The base system class, which all systems in the ECS architechture inherit from."""
