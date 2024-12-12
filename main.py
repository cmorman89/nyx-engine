from pprint import pprint

from random import randint
import time
from typing import Dict, List
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
    tile_dimension = 32
    tileset_store = TilesetStore()
    tile_size = (tile_dimension, tile_dimension)

    # Load tiles from .nyx files
    tile_files = [f"space-tiles-{i}" for i in range(1, 17)]
    # Save them to a temporary dictionary
    tile_imports: Dict[int, np.ndarray] = {}
    for i, filename in enumerate(tile_files):
        tile = NyxAssetImport.open_asset(filename)
        tile_imports[i] = tile
    for i, tile_texture in enumerate(tile_imports):
        # tile_texture = np.full(tile_size, randint(15, 255), dtype=np.uint8)
        tile_texture = tile_imports.get(i)
        tile_friendly_name = f"tile-{i}"
        tileset_store.create_tile(
            tile_texture=tile_texture,
            tile_id=i,
            tile_friendly_name=tile_friendly_name,
            overwrite=True,
        )
    # pprint(tile_files)
    # pprint(tile_imports)
    # pprint(tileset_store.tileset_textures)
    # input("Enter to continue")

    # Clear the terminal before the first run
    TerminalUtils.clear_term()

    # Loop to regenerate colors
    while True:
        tilemap = np.random.randint(1, 16, size=(10, 20), dtype=np.uint8)
        # Create "LevelRoot" Entity
        scene_entity = entity_manager.create_entity("scene-1")

        # Add components to entity
        (
            component_store.register_entity_component(
                scene_entity, SceneComponent("demo-map")
            )
            .register_entity_component(scene_entity, ZIndexComponent(0))
            # .register_entity_component(scene_entity, BackgroundColorComponent(33))
            .register_entity_component(scene_entity, BackgroundColorComponent(16))
            .register_entity_component(
                scene_entity, TilemapComponent(tilemap, tile_dimension=tile_dimension)
            )
        )

        # Call the render system to collect entities and pass to Aether
        z_indexed_entities = aether_collector.update()

        aether_renderer.viewport_h = 224
        aether_renderer.viewport_w = 228
        merged_frame = aether_renderer.accept_entities(
            aether_collector.update()
        ).render()
        hemera_term_api.print(merged_frame)
        # rendered_frame = aether_renderer.render()
        # hemera_term_api.output(rendered_frame)
        # time.sleep(2)
        time.sleep(0.5)
        # time.sleep(0.0666) # 15 fps
        # time.sleep(0.0333)  # 30 fps
        # time.sleep(0.0167) # 60 fps
        # time.sleep(0.00833)  # 120 FPS
