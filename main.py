from nyx.aether.aether_compositor import AetherCompositor
from nyx.engine.ecs.component.renderable_components import (
    BackgroundColorComponent,
    ZIndexComponent,
)
from nyx.engine.ecs.component.nyx_component_store import NyxComponentStore
from nyx.engine.ecs.entity.nyx_entity_manager import NyxEntityManager
from nyx.engine.ecs.system.render_system import AetherBridgeSystem
from nyx.hemera.hemera_renderer import HemeraRenderer


if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    entity_manager = NyxEntityManager()
    aether_compositor = AetherCompositor()
    hemera_renderer = HemeraRenderer()
    component_store = NyxComponentStore(entity_manager)
    render_system = AetherBridgeSystem(
        entity_manager, component_store, aether_compositor
    )

    # Create "LevelRoot" Entity
    level_root_entity = entity_manager.create_entity("LevelRoot")

    # Add components to entity
    component_store.register_component_to_entity(
        level_root_entity, BackgroundColorComponent(33)
    ).register_component_to_entity(level_root_entity, ZIndexComponent(0))

    render_system.update()

    hemera_renderer.draw_working_frame()
