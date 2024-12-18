"""
NyxEngine Module

This is the primary orchestration module of game-related tasks, systsems, and workflows.
"""

import time

from nyx.aether_renderer.aether_renderer import AetherRenderer
from nyx.aether_renderer.tilemap_manager import TilemapManager
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.moirai_ecs.component.component_manager import ComponentManager
from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager
from nyx.moirai_ecs.system.aether_bridge_system import AetherBridgeSystem
from nyx.moirai_ecs.system.base_systems import BaseSystem


class NyxEngine:
    # fps_target = 5
    game_update_per_sec = 60
    sec_per_game_loop = 1 / game_update_per_sec
    running_systems = []
    entity_manager = MoiraiEntityManager()
    component_manager = ComponentManager()
    aether_bridge = AetherBridgeSystem()
    aether_renderer = AetherRenderer()
    hemera_term_fx = HemeraTermFx()
    tilemap_manager = TilemapManager(dimensions=aether_renderer.dimensions)

    def run_game(self):
        while True:
            self.trigger_systems()
            self.render_frame()
            time.sleep(NyxEngine.sec_per_game_loop)

    def add_system(self, system: BaseSystem):
        NyxEngine.running_systems.append(system)

    def trigger_systems(self):
        for system in NyxEngine.running_systems:
            system.update()

    def kill_entities(self):
        cull_id_list = []
        h, w = (
            NyxEngine.aether_renderer.dimensions.effective_window_h,
            NyxEngine.aether_renderer.dimensions.effective_window_w,
        )
        for entity_id, comp in NyxEngine.component_manager.component_registry[
            "position"
        ].items():
            if comp.render_x_pos >= w or comp.render_y_pos >= h:
                cull_id_list.append(entity_id)
        for entity_id in cull_id_list:
            NyxEngine.entity_manager.destroy_entity(entity_id)

    def render_frame(self):
        NyxEngine.aether_bridge.update()
        renderable_entities = NyxEngine.aether_bridge.renderable_entities
        NyxEngine.aether_renderer.accept_entities(renderable_entities)
        new_frame = NyxEngine.aether_renderer.render()
        NyxEngine.hemera_term_fx.print(new_frame)
