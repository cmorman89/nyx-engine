from uuid import UUID, uuid4


class NyxEntity:
    """Provide a globally unique ID to act as a reference for a Nyx object, which is a container of components within the
    `NyxEntityManager`

    Attributes:
        entity_id (UUID): The globally unique ID of this entity.
        friendly_name (str, optional): The friendly name of this entity. Defaults to "".
    """

    def __init__(self, friendly_name: int = ""):
        """Initialize NyxEntity with an immutable globally unique entity id and optional friendly name"""
        self._entity_id: UUID = uuid4()
        self.friendly_name: str = friendly_name.strip() if friendly_name else ""

    @property
    def entity_id(self) -> UUID:
        return self._entity_id

    def __eq__(self, other):
        """Check for equality by comparing UUIDs or friendly name."""
        if isinstance(other, NyxEntity):
            return self.entity_id == other.entity_id
        elif isinstance(other, UUID):
            return self.entity_id == other
        elif isinstance(other, str):
            return self.friendly_name == other or str(self.entity_id) == other
        return False

    def __repr__(self):
        return f"NyxEntity(friendly_name={self.name}, entity_id={self._entity_id})"

    def __hash__(self):
        return hash(self.entity_id)
