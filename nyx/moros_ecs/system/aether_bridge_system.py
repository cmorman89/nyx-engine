"""
Aether ECS-Renderer Bridge Module

This module collects and z-indexes the entities and components that are renderable, before handing
them off to AetherRenderer for granular processing and frame generation.
"""

from nyx.moros_ecs.component.base_components import RenderableComponent
from nyx.nyx_engine.stores.component_store import ComponentStore
from nyx.moros_ecs.moros_entity_manager import MorosEntityManager
from nyx.moros_ecs.system.base_systems import BaseSystem


class AetherBridgeSystem(BaseSystem):
    """Responsible for collecting all renderable components and passing them to Aether for
    composition and prioritization.

    Attributes:
        entity_manager (MorosEntityManager): The entitity manager that holds the entity list.
        component_store (ComponentStore): The component store that holds the component objects.
    """

    def __init__(
        self,
        entity_manager: MorosEntityManager,
        component_store: ComponentStore,
    ):
        """Initialize the bridge with references to the entity manager and component store."""
        super().__init__(entity_manager)
        self.component_store = component_store

    def update(self):
        """Generate a z-indexed dict of entities and their renderable components.

        Returns:
            Dict[int, Dict[UUID, Dict[str, RenderableComponent]]]): The dict of renderable data sent
                to Aether. For explicit clarity, the structure is:

                    {z-index (int): {
                        entity id (UUID): {
                            component name (str): component object (RenderableComponent)}}}

        """
        z_indexed_entities = {}

        # Fetch entity registry
        entity_registry = self.entity_manager.get_all_entities()

        # Generate the z-index-entity-component dict to hand to Aether
        for entity_id, entity in entity_registry.items():
            z_index = -1
            entity_dict = {entity_id: {}}

            # Iterate the entity's components from the component store
            for comp_name, comp_obj in self.component_store.get_all_components(
                entity
            ).items():
                if isinstance(comp_obj, RenderableComponent):
                    entity_dict[entity_id][comp_name] = comp_obj
                    if comp_name == "ZIndexComponent":
                        z_index = comp_obj.z_index

            # Add a new z-index key in the dict if it does not exist already
            if len(entity_dict[entity_id]) > 0:
                if z_index not in z_indexed_entities:
                    z_indexed_entities[z_index] = {}
                z_indexed_entities[z_index][entity_id] = entity_dict[entity_id]

        # Return the z-index-entity-component dict if it is not empty
        if len(z_indexed_entities) > 0:
            return z_indexed_entities
