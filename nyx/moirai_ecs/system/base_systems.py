"""
Abstract Base System Module

This module defines the abstract base classes that all systems in the ECS architechture inherit
from.
"""

from abc import ABC

from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager


class BaseSystem(ABC):
    """The base system class, which all systems in the ECS architechture inherit from.

    Attributes:
        entity_manager (MorosEntityManager): The entity manager holding the entity registry.
    """

    def __init__(self, entity_manager: MoiraiEntityManager):
        """Initialize with an entity manager, and ensure all systems have the entity manager
        defined upon init.

        Args:
            entity_manager (MorosEntityManager): The entity manager holding the entity registry.
        """
        self.entity_manager: MoiraiEntityManager = entity_manager
