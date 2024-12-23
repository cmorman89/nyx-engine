"""
NyxEntity Module

This module defines the entity class within the ECS architecture. An entity holds a globally unique
reference ID (int) which is then linked to different components or assets within the game engine.
"""


class NyxEntity:
    """Define the game entity object, which holds a globally unique reference ID (int). This ID is
    then linked to different components or assets within the game engine.

    Attributes:
        entity_id (int): The globally unique ID of this entity.
        friendly_name (str, optional): The friendly name of this entity. Defaults to "".
    """

    _next_entity_id = 0

    def __init__(self, friendly_name: str = ""):
        """Initialize NyxEntity with an immutable globally unique entity id and optional friendly
        name.

        Args:
            friendly_name (str, optional): The human-readable friendly name for the entity. Defaults
                to "".
        """
        self._entity_id: int = NyxEntity._next_entity_id
        NyxEntity._next_entity_id += 1
        self.friendly_name: str = friendly_name.strip() if friendly_name else ""

    @property
    def entity_id(self) -> int:
        """Safely return the entity_id as an int."""
        return self._entity_id

    def __eq__(self, other):
        """Check for equality by comparing ints or friendly name."""
        if isinstance(other, NyxEntity):
            return self.entity_id == other.entity_id
        elif isinstance(other, int):
            return self.entity_id == other
        return False

    def __hash__(self):
        """Use the entity_id when determining the hash of an entitiy."""
        return hash(self.entity_id)

    def __repr__(self):
        return f"NyxEntity(friendly_name={self.friendly_name}, entity_id={self._entity_id})"
