"""
MorosEntity Manager Module

This module orcehstrates the creation and destruction of entities in the ECS architecture, keeping a
registry of current, alive entities and their unique entity IDs.

Classes:
    MorosEntityManager: Performs CRUD operations of game entities within its held entity registry.

Mythology:
    In the Greek pantheon, Moros is the son of Nyx (Night) and personifies the inexorable force of
    doom. He is the relentless power that drives all beings, mortal and divine alike, toward their
    fated end, embodying the inevitability of death and destiny. It is said that not even the gods,
    including Zeus, could defy the unyielding nature of Moros and the cosmic laws he represents.
"""

from typing import Dict
from uuid import UUID
from nyx.moros_ecs.entity.nyx_entity import NyxEntity


class MorosEntityManager:
    """Holds and performs CRUD operations on registries for entities and their entity ids, as well
    as entities and their friendlynames.
    """

    def __init__(self):
        self._entity_registry: Dict[UUID, NyxEntity] = {}
        self._friendly_name_registry: Dict[str, NyxEntity] = {}

    def create_entity(self, friendly_name: str = "") -> NyxEntity:
        """Create a NyxEntity and add it to the entity registry"""
        if friendly_name:
            friendly_name = friendly_name.strip()
        if len(friendly_name) > 0 and friendly_name in self._entity_registry:
            raise ValueError(
                f'Cannot create NyxEntity with friendly_name="{friendly_name}"; Friendly name already taken.'
            )
        entity = NyxEntity(friendly_name=friendly_name.strip())
        self._register_entity(entity)
        return entity

    def destroy_entity(self):
        return self

    def is_alive(self, entity_identifier: NyxEntity | UUID | str) -> bool:
        """Check if a NyxEntity is still active in this entity manager.

        Can locate entities by NyxEntity, a UUID (as UUID or str), or the friendly name.

        Args:
            entity_identifier (NyxEntity | UUID | str): Identifier to use to locate entity.

        Returns:
            bool: _description_
        """
        return entity_identifier in self._entity_registry

    def get_entity(self, entity_identifier: NyxEntity | UUID | str) -> NyxEntity:
        if isinstance(entity_identifier, NyxEntity):
            return NyxEntity
        elif isinstance(entity_identifier, UUID):
            return self._entity_registry[entity_identifier]
        elif isinstance(entity_identifier, str):
            return self._friendly_name_registry[entity_identifier]
        else:
            raise ValueError(f'NyxEntity with identifier="{entity_identifier}.')

    def get_all_entities(self) -> Dict[UUID, NyxEntity]:
        """Return a registry of all entities in this manager.

        Returns:
            registry[NyxEntity]: the registry of NyxEntity objects.
        """
        return self._entity_registry

    def _register_entity(self, entity: NyxEntity):
        """Add an entity to the entity registry."""
        self._entity_registry[entity.entity_id] = entity
        if entity.friendly_name and entity.friendly_name != "":
            self._friendly_name_registry[entity.friendly_name] = entity

    def _unregister_entity(self, entity: NyxEntity):
        """Remove an entity from the entity registry."""
        if entity.entity_id in self._entity_registry:
            del self._entity_registry[entity.entity_id]
            if (
                entity.friendly_name
                and entity.friendly_name in self._friendly_name_registry
            ):
                del self._friendly_name_registry[entity.friendly_name]
