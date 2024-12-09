from nyx.aether.aether_renderer import AetherRenderer
from nyx.engine.ecs.component.renderable_components import (
    BackgroundColorComponent,
    ZIndexComponent,
)
from nyx.engine.ecs.component.scene_component import SceneComponent
from nyx.engine.stores.nyx_component_store import NyxComponentStore
from nyx.engine.managers.nyx_entity_manager import NyxEntityManager
from nyx.engine.ecs.system.render_system import AetherBridgeSystem
from nyx.hemera.hemera_term_fx import HemeraTermFx


if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    entity_manager = NyxEntityManager()
    aether_renderer = AetherRenderer()
    hemera_term_api = HemeraTermFx()
    component_store = NyxComponentStore(entity_manager)
    aether_collector = AetherBridgeSystem(entity_manager, component_store)

    # Create "LevelRoot" Entity
    level_root_entity = entity_manager.create_entity("LevelRoot")

    # Add components to entity
    (
        component_store.register_entity_component(
            level_root_entity, SceneComponent("Demo")
        )
        .register_entity_component(level_root_entity, ZIndexComponent(0))
        .register_entity_component(level_root_entity, BackgroundColorComponent(33))
    )

    # Call the render system to collect entities and pass to Aether
    z_indexed_entities = aether_collector.update()

    aether_renderer.view_h = 16
    aether_renderer.view_w = 16
    hemera_term_api.output(
        aether_renderer.accept_entities(aether_collector.update()).render()
    )

    # rendered_frame = aether_renderer.render()

    # hemera_term_api.output(rendered_frame)
