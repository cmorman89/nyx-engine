"""
Component Store Module

Manages and organizes the components that define the behaviors of game entities. The components are
indexed and can be queried by the unique entity_id/int of the parent entity.

Classes:
    ComponentStore: The centralized storage of all Components in NyxEngine, organized by entity_id/
        int.
"""

from typing import Dict
from nyx.moros_ecs.component.base_components import BaseComponent
from nyx.moros_ecs.entity.nyx_entity import NyxEntity
from nyx.moros_ecs.moros_entity_manager import MorosEntityManager


class ComponentStore:
    """Centrally stores, manages, and retieves components for NyxEntities, indexed by their
    entity_id/int. Entity friendly name retreival is also supported.
    """

    def __init__(self, entity_manager: MorosEntityManager):
        """Initialize with a reference to the entity manager and an empty component registry."""
        self.entity_manager: MorosEntityManager = entity_manager
        self.component_registry: Dict[int, Dict[str, BaseComponent]] = {}

    def register_entity_component(
        self, entity_identifier: NyxEntity | int | str, component: BaseComponent
    ):
        """Register a component to an entity in the component registry by its int.

        Args:
            entity_identifier (NyxEntity | int | str): Look up by entity obj, int, or friendly
                name.
            component (Component): The component to add to the entity.
        """
        # Fetch/validate the entity
        entity = self.entity_manager.get_entity(entity_identifier)
        # Add the entity if it its first component
        if entity.entity_id not in self.component_registry:
            self.component_registry[entity.entity_id] = {}
        # Add the component
        self.component_registry[entity.entity_id][type(component).__name__] = component
        return self

    def unregister_entity_component(
        self,
        entity_identifier: NyxEntity | int | str,
        component_type: str | BaseComponent,
    ):
        """Remove a given component from an entity.

        Args:
            entity_identifier (NyxEntity | int | str): Look up by entity obj, int, or friendly
                name.
            component_type (str | Component): The class name as a string, an instance of the
                Component, or a Component class itself.
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        component_type = self.validate_component_type(component_type)
        if self.component_registry[entity.entity_id][component_type]:
            del self.component_registry[entity.entity_id][component_type]
            return self
        raise KeyError(
            "Unable to delete component."
            + f'Component="{component_type}" not found for NyxEntity="{entity!r}".'
        )

    def unregister_entity(self, entity_identifier: NyxEntity | int | str):
        """Remove an entity and all its components from the component registry.

        Args:
            entity_identifier (NyxEntity | int | str): Look up by entity obj, int, or friendly
                name.
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
        entity_identifier: NyxEntity | int | str,
        component_type: str | BaseComponent,
    ) -> BaseComponent:
        """Fetch a particular component for an entity in the component registry.

        Args:
            entity_identifier (NyxEntity | int | str): Look up by entity obj, int, or friendly
                name.
            component_type (str | Component): The class name as a string, an instance of the
                Component, or a Component class itself.


        Raises:
            KeyError: The NyxEntity or Component was not found in the component registry.

        Returns:
            Component: The requested component for the given entity.
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
        self, entity_identifier: NyxEntity | int | str
    ) -> Dict[str, BaseComponent]:
        """Fetch a dict of components for a NyxEntity.

        Args:
            entity_identifier (NyxEntity | int | str): Look up by entity obj, int, or
                friendly_name.

        Raises:
            KeyError: The NyxEntity was not found in the component registry.

        Returns:
            Dict[str, Component]: The class name and instance of all components registered to
                the NyxEntity..
        """
        entity = self.entity_manager.get_entity(entity_identifier)
        component_dict = self.component_registry[entity.entity_id]
        if component_dict:
            return component_dict
        raise KeyError(f"Entity not found in component registry, entity={entity!r}")

    def validate_component_type(self, component_type: str | BaseComponent) -> str:
        """Return the class name of a provided Component.

        Args:
            component_type (str | Component): The class name as a string, an instance of the
                Component, or a Component class itself.

        Returns:
            str: The name of the component class as a string.
        """
        if isinstance(component_type, str):
            return component_type
        if isinstance(component_type, type):
            return component_type.__name__
        elif isinstance(component_type, BaseComponent):
            return type(component_type).__name__
