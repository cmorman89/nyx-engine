""" """

from nyx.moros_ecs.component.base_components import RenderableComponent
from nyx.nyx_engine.stores.component_store import ComponentStore
from nyx.moros_ecs.moros_entity_manager import MorosEntityManager
from nyx.moros_ecs.system.moros_system_base import MorosSystem


class AetherBridgeSystem(MorosSystem):
    """Responsible for collecting all renderable components and passing them to Aether for
    composition and prioritization."""

    def __init__(
        self,
        entity_manager: MorosEntityManager,
        component_store: ComponentStore,
    ):
        super().__init__(entity_manager)
        self.component_store = component_store

    def update(self):
        """Get all renderable components"""
        z_indexed_entities = {}
        entity_registry = self.entity_manager.get_all_entities()
        for entity_id, entity in entity_registry.items():
            priority = -1
            entity_dict = {entity_id: {}}
            for comp_name, comp_obj in self.component_store.get_all_components(
                entity
            ).items():
                if isinstance(comp_obj, RenderableComponent):
                    entity_dict[entity_id][comp_name] = comp_obj
                    if comp_name == "ZIndexComponent":
                        priority = comp_obj.z_index
            if len(entity_dict[entity_id]) > 0:
                if priority not in z_indexed_entities:
                    z_indexed_entities[priority] = {}
                z_indexed_entities[priority][entity_id] = entity_dict[entity_id]

        if len(z_indexed_entities) > 0:
            return z_indexed_entities
