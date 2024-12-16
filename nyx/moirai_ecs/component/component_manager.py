"""
Component Manager Module

Manages and organizes the components that define the behaviors of game entities. The components are
indexed by entity ID.

Classes:
    ComponentManager:
"""

from typing import Dict

from nyx.moirai_ecs.component.base_components import NyxComponent


class ComponentManager:
    """Holds and manages a registry of sub dictionaries, each of which maps entity IDs to specific
    component types.

    Attributes:
        component_registry (Dict[str, Dict[int, NyxComponent]]): The registry of all components
            registered to entities.

    """

    # Component Registry
    component_registry: Dict[str, Dict[int, NyxComponent]] = {
        "dimensions": {},
        "position": {},
        "texture": {},
        "velocity": {},
        "z-index": {},
    }

    def add_component(
        self, entity_id: int, component_name: str, component: NyxComponent
    ):
        """Register a new component to an entity.

        Args:
            entity_id (int): The entity ID for the entity to add the component to.
            component_name (str): The name of the sub-dictionary that holds that component.
            component (NyxComponent): The component to add to the sub-dictionary.

        Raises:
            ValueError: If the component type is already registered for that entity ID.
        """
        if entity_id in ComponentManager.component_registry[component_name]:
            raise ValueError(
                f'Component="{component_name}" already exists for entity={entity_id}'
            )

        ComponentManager.component_registry[component_name][entity_id] = component

    def get_component(self, entity_id: int, component_name: str) -> NyxComponent:
        """Get a component for an entity.

        Args:
            entity_id (int): The entity ID reference key for the component.
            component_name (str): The name of the sub-dictionary that holds that component.

        Raises:
            KeyError: If the entity_id is not found for that component type.

        Returns:
            NyxComponent: The component retrieved.
        """

        if entity_id in ComponentManager.component_registry[component_name]:
            return ComponentManager.component_registry[component_name][entity_id]
        raise KeyError(
            f'Entity={entity_id} not found in "{component_name}" component registry.'
        )

    def update_component(
        self, entity_id: int, component_name: str, component: NyxComponent
    ):
        """Update the component registered to the entity.

        Args:
            entity_id (int): The entity ID reference key for the component.
            component_name (str): The name of the sub-dictionary that holds that component.
            component (NyxComponent): The component to add to the sub-dictionary.

        Raises:
            KeyError: If the entity_id is not found for that component type.
        """
        if entity_id not in ComponentManager.component_registry[component_name]:
            raise KeyError(
                f'Entity={entity_id} not found in "{component_name}" component registry.'
            )
        ComponentManager.component_registry[component_name][entity_id] = component

    def destroy_component(self, entity_id: int, component_name: str):
        """Remove the a component from from the registry.

        Args:
            entity_id (int): The entity ID reference key for the component.
            component_name (str): The name of the sub-dictionary that holds that component.

        Raises:
            KeyError: If the entity_id is not found for that component type.
        """
        if entity_id not in ComponentManager.component_registry[component_name]:
            raise KeyError(
                f'Entity={entity_id} not found in "{component_name}" component registry.'
            )
        del ComponentManager.component_registry[component_name][entity_id]

    @staticmethod
    def remove_entity(entity_id: int):
        """Remove all components belonging to an entity.

        Args:
            entity_id (int): The entity ID of the entity to clear from the registry.
        """
        for sub_dict in ComponentManager.component_registry.values():
            if entity_id in sub_dict.keys():
                del sub_dict[entity_id]
