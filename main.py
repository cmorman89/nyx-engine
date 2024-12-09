from random import randint
import numpy as np
from nyx.aether.aether_renderer import AetherRenderer
from nyx.engine.ecs.component.renderable_components import (
    BackgroundColorComponent,
    TilemapComponent,
    ZIndexComponent,
)
from nyx.engine.ecs.component.scene_component import SceneComponent
from nyx.engine.stores.nyx_component_store import NyxComponentStore
from nyx.engine.managers.nyx_entity_manager import NyxEntityManager
from nyx.engine.ecs.system.aether_bridge_system import AetherBridgeSystem
from nyx.engine.stores.tileset_store import TilesetStore
from nyx.hemera.hemera_term_fx import HemeraTermFx


if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    entity_manager = NyxEntityManager()
    aether_renderer = AetherRenderer()
    hemera_term_api = HemeraTermFx()
    component_store = NyxComponentStore(entity_manager)
    aether_collector = AetherBridgeSystem(entity_manager, component_store)

    # Create a simple tile map and tiles
    tilemap = np.array([[1, 2, 1, 2], [4, 3, 2, 1], [0, 0, 0, 0]], dtype=np.uint8)
    tileset_store = TilesetStore()
    tile_size = (16, 16)
    for i in range(5):
        tile_texture = np.full(tile_size, randint(15, 255), dtype=np.uint8)
        tile_friendly_name = f"tile-{i}"
        tileset_store.create_tile(
            tile_texture=tile_texture, tile_id=i, tile_friendly_name=tile_friendly_name
        )

    # Create "LevelRoot" Entity
    scene_entity = entity_manager.create_entity("scene-1")

    # Add components to entity
    (
        component_store.register_entity_component(
            scene_entity, SceneComponent("demo-map")
        )
        .register_entity_component(scene_entity, ZIndexComponent(0))
        .register_entity_component(scene_entity, BackgroundColorComponent(33))
        .register_entity_component(scene_entity, TilemapComponent(tilemap))
    )

    # Call the render system to collect entities and pass to Aether
    z_indexed_entities = aether_collector.update()

    aether_renderer.view_h = 25
    aether_renderer.view_w = 25
    merged_frame = aether_renderer.accept_entities(aether_collector.update()).render()
    hemera_term_api.output(merged_frame)

    # rendered_frame = aether_renderer.render()

    # hemera_term_api.output(rendered_frame)
