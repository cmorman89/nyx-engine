"""
NyxEngine Module

This is the primary orchestration module of game-related tasks, systsems, and workflows.
"""

import time

from nyx.aether_renderer.aether_renderer import AetherRenderer
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.moirai_ecs.component.component_manager import ComponentManager
from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager
from nyx.moirai_ecs.system.aether_bridge_system import AetherBridgeSystem
from nyx.moirai_ecs.system.base_systems import BaseSystem


class NyxEngine:
    fps_target = 30
    game_update_per_sec = 30
    sec_per_game_loop = 1 / game_update_per_sec
    running_systems = []
    entity_manager = MoiraiEntityManager()
    component_manager = ComponentManager()
    aether_bridge = AetherBridgeSystem()
    aether_renderer = AetherRenderer()
    hemera_term_fx = HemeraTermFx()

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

    def render_frame(self):
        NyxEngine.aether_bridge.update()
        renderable_entities = NyxEngine.aether_bridge.renderable_entities
        NyxEngine.aether_renderer.accept_entities(renderable_entities)
        new_frame = NyxEngine.aether_renderer.render()
        NyxEngine.hemera_term_fx.print(new_frame)
