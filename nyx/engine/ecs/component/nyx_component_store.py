from typing import Dict
from uuid import UUID
from nyx.engine.ecs.component.nyx_component import NyxComponent
from nyx.engine.ecs.entity.nyx_entity import NyxEntity
from nyx.engine.ecs.entity.nyx_entity_manager import NyxEntityManager


class NyxComponentStore:
    def __init__(self, entity_manager: NyxEntityManager):
        """Initialize with a reference to the entity manager and an empty component registry."""
        self.entity_manager: NyxEntityManager = entity_manager
        self.component_registry: Dict[UUID, Dict[str, NyxComponent]] = {}

    def register_component_to_entity(
        self, entity_identifier: NyxEntity | UUID | str, component: NyxComponent
    ):
        """Register a component to an entity in the component registry by its UUID.

        Args:
            entity_identifier (NyxEntity | UUID | str): Look up by entity obj, UUID, or friendly_name.
            component (NyxComponent): The component to add to the entity.
        """
        # Fetch/validate the entity
        entity = self.entity_manager.get_entity(entity_identifier)
        # Add the entity if it its first component
        if entity.entity_id not in self.component_registry:
            self.component_registry[entity.entity_id] = {}
        # Add the component
        self.component_registry[entity.entity_id][type(component).__name__] = component
        return self

    def unregister_component_from_entity(
        self,
        entity_identifier: NyxEntity | UUID | str,
        component_type: str | NyxComponent,
    ):
        """Remove a given component from an entity.

        Args:
            entity_identifier (NyxEntity | UUID | str): Look up by entity obj, UUID, or
                friendly_name.
            component_type (str | NyxComponent): The class name as a string, an instance of the
                NyxComponent, or a NyxComponent class itself.
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        component_type = self.validate_component_type(component_type)
        if self.component_registry[entity.entity_id][component_type]:
            del self.component_registry[entity.entity_id][component_type]
            return self
        raise KeyError(
            "Unable to delete component."
            + f'NyxComponent="{component_type}" not found for NyxEntity="{entity!r}".'
        )

    def unregister_entity(self, entity_identifier: NyxEntity | UUID | str):
        """Remove an entity and all its components from the component registry.

        Args:
            entity_identifier (NyxEntity | UUID | str): Look up by entity obj, UUID, or
                friendly_name.
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        if entity.entity_id in self.component_registry:
            del self.component_registry[entity.entity_id]
            return self
        raise KeyError(
            f"Unable to delete NyxEntity from component registry. Not found: entity = {entity!r}"
        )

    def get_component(
        self,
        entity_identifier: NyxEntity | UUID | str,
        component_type: str | NyxComponent,
    ) -> NyxComponent:
        """Fetch a particular component for an entity in the component registry.

        Args:
            entity_identifier (NyxEntity | UUID | str): Look up by entity obj, UUID, or
                friendly_name.
            component_type (str | NyxComponent): The class name as a string, an instance of the
                NyxComponent, or a NyxComponent class itself.


        Raises:
            KeyError: The NyxEntity or NyxComponent was not found in the component registry.

        Returns:
            NyxComponent: The requested component for the given entity.
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        component_type = self.validate_component_type(component_type)
        component = self.component_registry[entity.entity_id][component_type]
        if component:
            return component
        raise KeyError(
            f'Component = "{component_type}" not found for NyxEntity = "{entity!r}'
        )

    def get_all_components(
        self, entity_identifier: NyxEntity | UUID | str
    ) -> Dict[str, NyxComponent]:
        """Fetch a dict of components for a NyxEntity.

        Args:
            entity_identifier (NyxEntity | UUID | str): Look up by entity obj, UUID, or
                friendly_name.

        Raises:
            KeyError: The NyxEntity was not found in the component registry.

        Returns:
            Dict[str, NyxComponent]: The class name and instance of all components registered to
                the NyxEntity..
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        component_dict = self.component_registry[entity.entity_id]
        if component_dict:
            return component_dict
        raise KeyError(f"Entity not found in component registry, entity={entity!r}")

    def validate_component_type(self, component_type: str | NyxComponent) -> str:
        """Return the class name of a provided NyxComponent.

        Args:
            component_type (str | NyxComponent): The class name as a string, an instance of the
                NyxComponent, or a NyxComponent class itself.

        Returns:
            str: The name of the component class as a string.
        """
        if isinstance(component_type, str):
            return component_type
        if isinstance(component_type, type):
            return component_type.__name__
        elif isinstance(component_type, NyxComponent):
            return type(component_type).__name__
