from random import randint
import time
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
from nyx.hemera.term_utils import TerminalUtils
from nyx.utils.nyx_asset_import import NyxAssetImport


if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    entity_manager = NyxEntityManager()
    aether_renderer = AetherRenderer()
    hemera_term_api = HemeraTermFx()
    component_store = NyxComponentStore(entity_manager)
    aether_collector = AetherBridgeSystem(entity_manager, component_store)

    # Create a simple tile map and tiles
    tilemap = np.array([[0, 2, 1, 2], [4, 3, 0, 1], [0, 1, 0, 1]], dtype=np.uint8)
    tile_dimension = 24
    tileset_store = TilesetStore()
    tile_size = (tile_dimension, tile_dimension)
    tile_load = NyxAssetImport.open_asset("spaceship")

    # Clear the terminal before the first run
    TerminalUtils.clear_term()

    # Loop to regenerate colors
    while True:
        TilesetStore.reset_store()
        tileset_store.create_tile(
            tile_texture=tile_load,
            tile_id=0,
            tile_friendly_name="spaceship",
            overwrite=True,
        )
        for i in range(1, 5):
            tile_texture = np.full(tile_size, randint(15, 255), dtype=np.uint8)
            tile_friendly_name = f"tile-{i}"
            tileset_store.create_tile(
                tile_texture=tile_texture,
                tile_id=i,
                tile_friendly_name=tile_friendly_name,
                overwrite=True,
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
            .register_entity_component(
                scene_entity, TilemapComponent(tilemap, tile_dimension=tile_dimension)
            )
        )

        # Call the render system to collect entities and pass to Aether
        z_indexed_entities = aether_collector.update()

        # aether_renderer.view_h = 25
        # aether_renderer.view_w = 25
        merged_frame = aether_renderer.accept_entities(
            aether_collector.update()
        ).render()
        hemera_term_api.output(merged_frame)
        # rendered_frame = aether_renderer.render()
        # hemera_term_api.output(rendered_frame)
        # time.sleep(0.0666) # 15 fps
        # time.sleep(0.0333) # 30 fps
        # time.sleep(0.0167) # 60 fps
        time.sleep(0.00833) # 120 FPS
