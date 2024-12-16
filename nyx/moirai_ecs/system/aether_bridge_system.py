"""
Aether ECS-Renderer Bridge Module

This module collects and z-indexes the entities and components that are renderable, before handing
them off to AetherRenderer for granular processing and frame generation.
"""

from nyx.moirai_ecs.component.component_manager import ComponentManager
from nyx.moirai_ecs.system.base_systems import BaseSystem


class AetherBridgeSystem(BaseSystem):
    """Responsible for collecting all renderable components and passing them to Aether for
    composition and prioritization.
    """

    def __init__(self):
        self.renderable_entities = {}

    def update(self):
        component_registry = ComponentManager.component_registry
        renderable_entities = {}

        for entity_id, z_index_comp in component_registry["z-index"].items():
            if (
                entity_id in component_registry["position"]
                and entity_id in component_registry["texture"]
            ):
                z_index = z_index_comp.z_index
                texture = component_registry["texture"][entity_id].texture
                x = component_registry["position"][entity_id].render_x_pos
                y = component_registry["position"][entity_id].render_y_pos
                renderable_entity = (x, y, texture)
                self._validate_z_index(
                    z_index=z_index, renderable_entities=renderable_entities
                )
                renderable_entities[z_index].append(renderable_entity)
        self.renderable_entities = renderable_entities

    def _validate_z_index(self, z_index: int, renderable_entities: dict):
        if z_index not in renderable_entities:
            renderable_entities[z_index] = []
