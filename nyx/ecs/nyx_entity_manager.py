from ast import Dict
from typing import Optional
from uuid import UUID, uuid4

from nyx.ecs.component.tile_component import NyxComponent


class NyxEntity:
    """Provide a globally unique ID to act as a reference for a Nyx object, which is a container of components within the
    `NyxEntityManager`

    Attributes:
        entity_id (UUID): The globally unique ID of this entity.
        manager (NyxEntityManager): Backreference to the `NyxEntityManager` that created this entity.
        name (str, optional): The friendly name of this entity. Defaults to "".

    Methods:
        add_component: Add/register a component to to this entity.
        get_component: Get the component(s) registered to this entity.
    """

    def __init__(self, manager: "NyxEntityManager", name: str = ""):
        self._entity_id = uuid4()
        self.manager = manager
        self.name = name

    @property
    def entity_id(self) -> UUID:
        return self._entity_id

    def add_component(self, component: NyxComponent):
        """Add/register a component to this entity.

        Args:
            component (NyxComponent): The `NyxComponent`-type to register to this reference ID.
        """
        self.manager.add_component(self, component)
        return self

    def get_components(self) -> Optional["NyxComponent"]:
        """Get the component(s) registered to this entity."""
        return self.manager.get_components(entity=self)

    def __eq__(self, other):
        """Check for equality by comparing UUIDs"""
        if isinstance(other, UUID):
            return self._entity_id == other
        return False

    def __repr__(self):
        return f"NyxEntity(name={self.name}, entity_id={self._entity_id})"


class NyxEntityManager:
    """Manage the list of entity reference IDs (`NyxEntity`) and their registered components (`NyxComponent`) .

    Attributes:
        entities (list[NyxEntity]): The list of entities referencing containers within this manager.
        components (Dict[UUID, Dict(str, NyxComponent)]): The containers of components belonging to each entity,  referenced by
            their UUID.

    Methods:
        create_entity: Create a new entity held by this manager.
        add_component: Add/register a component to an entity.
        get_component: Get the component(s) registered to an entity.
    """

    def __init__(self):
        """Initialize the entity manager with an empty entities list and empty components dictionary."""
        self.entities: list[NyxEntity] = []
        self.components: Dict[UUID, Dict[str, "NyxComponent"]] = {}

    def create_entity(self, name: str = "") -> NyxEntity:
        """Create a new entity held by this manager.

        Attributes:
            name (str, optional): The optional, friendly name of the entity. Defaults to ""

        Returns:
            NyxEntity: the entity object/reference.
        """
        entity = NyxEntity(name=name, manager=self)
        self.entities.append(entity)
        self.components[entity.entity_id] = {}
        return entity

    def add_component(self, entity: NyxEntity, component: NyxComponent):
        """Add/register a component to a referenced entity in this manager.

        Args:
            entity (NyxEntity): The entity to register the component to.
            component (NyxComponent):
        """
        self.components[entity.entity_id][type(component).__name__] = component

    def get_components(self, entity: NyxEntity) -> Optional[NyxComponent]:
        """Get the component(s) registered to an entity in this manager.

        Args:
            entity (NyxEntity): The entity to lookup.

        Returns:
            Optional[NyxComponent]: The NyxComponent retrieved for this entity.
        """
        return self.components.get(entity.entity_id, {})
