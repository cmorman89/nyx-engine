"""
Moirai Entity Manager Module

This module orcehstrates the creation and destruction of entities in the ECS architecture, keeping a
registry of current, alive entities and their unique entity IDs.

Classes:
    MorosEntityManager: Performs CRUD operations of game entities within its held entity registry.

Mythology:
    In the Greek pantheon, the Moirai are better known as the Fates and are children of Nyx (source
    depending). Together, the three sisters determine the destiny and fate of both mortals and
    divine beings, alike. Clotho spins the thread representing the start of life; Lachesis allots
    the path that life will follow; and Atropos cuts the thread, ending that life's journey.
"""

from typing import Dict, TYPE_CHECKING
from nyx.moirai_ecs.entity.nyx_entity import NyxEntity

if TYPE_CHECKING:
    from nyx.nyx_engine.nyx_engine import NyxEngine


class MoiraiEntityManager:
    """Holds and performs CRUD operations on registries for entities and their entity ids.

    Attributes:
        entity_registry (Dict[int, NyxEntity]) = The registry of entities keyed by their entity ID.

    Methods:
        create_entity: Create and register a new entity to the entity registry.
        destroy_entity: Remove a registered entity from the entity registry.
        is_alive: Check if an entity is still active in the registry.
        get_entity: Fetch an entity from the registry by its entity ID.
        get_all_entities: Fet the entire entity registry list.
    """

    entity_registry: Dict[int, NyxEntity] = {}

    @classmethod
    def reset_entity_registry(cls):
        """Clear the entity registry of all entities."""
        cls.entity_registry.clear()

    def __init__(self, engine: "NyxEngine"):
        self.engine = engine
        self.component_manager = self.engine.component_manager
        self.component_registry = self.engine.component_registry
        self.entity_registry: Dict[int, NyxEntity] = {}

    def create_entity(self, friendly_name: str = "") -> NyxEntity:
        """Create a NyxEntity and add it to the entity registry.

        Args:
            friendly_name (str): The human-readable friendly name for debugging. Defaults to "".

        Returns:
            NyxEntity: the newly created entity.
        """

        new_entity = NyxEntity(friendly_name=friendly_name.strip())
        self.entity_registry[new_entity.entity_id] = new_entity
        return new_entity

    def destroy_entity(self, entity_id: int):
        """Remove a registered entity from the entity registry, and clear its components.

        Args:
            entity_id (int): The entity ID to remove.
        """
        if entity_id in self.entity_registry:
            del self.entity_registry[entity_id]
            self.component_manager.remove_entity(entity_id=entity_id)
        return self

    def is_alive(self, entity_id: int) -> bool:
        """Check if a NyxEntity is still active in this entity manager.

        Args:
            entity_id (int): The entity ID to check for alive status.

        Returns:
            bool: If the entity is alive.
        """
        return entity_id in self.entity_registry

    def get_entity(self, entity_id: int) -> NyxEntity:
        """Get an entity from the entity list

        Args:
            entity_id (int): The entity ID of the entity to fetch.

        Returns:
            NyxEntity: The entity with the specified entity ID.
        """
        if entity_id in self.entity_registry:
            return self.entity_registry[entity_id]

    def get_all_entities(self) -> Dict[int, NyxEntity]:
        """Return a registry of all entities in this manager.

        Returns:
            Dict[int, NyxEntity]: The registry of NyxEntity objects.
        """
        return self.entity_registry
