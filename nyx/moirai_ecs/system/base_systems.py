"""
Abstract Base System Module

This module defines the abstract base classes that all systems in the ECS architechture inherit
from.
"""

from abc import ABC

from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager


class BaseSystem(ABC):
    """The base system class, which all systems in the ECS architechture inherit from."""
