import time
from typing import Dict
import numpy as np
from nyx.aether_renderer.aether_renderer import AetherRenderer
from nyx.moirai_ecs.component.transform_components import (
    ZIndexComponent,
)
from nyx.moirai_ecs.component.scene_components import (
    BackgroundColorComponent,
    SceneComponent,
    TilemapComponent,
)
from nyx.nyx_engine.stores.component_store import ComponentStore
from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager
from nyx.moirai_ecs.system.aether_bridge_system import AetherBridgeSystem
from nyx.nyx_engine.stores.tileset_store import TilesetStore
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.hemera_term_fx.term_utils import TerminalUtils
from nyx.utils.nyx_asset_import import NyxAssetImport


if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    entity_manager = MoiraiEntityManager()
    aether_renderer = AetherRenderer()
    hemera_term_api = HemeraTermFx()
    component_store = ComponentStore(entity_manager)
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

    # Clear the terminal before the first run
    TerminalUtils.clear_term()
    # Scroll left -> right = positive value
    # SCroll right -> left = negative value
    x_pos = 0
    x_vel = -4
    trip_randomize = 0
    # Loop to regenerate colors
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
    while True:
        # Call the render system to collect entities and pass to Aether
        z_indexed_entities = aether_collector.update()

        aether_renderer.dimensions.window_h = 180
        aether_renderer.dimensions.window_w = 240
        merged_frame = aether_renderer.accept_entities(
            aether_collector.update()
        ).render()
        merged_frame = np.roll(merged_frame, x_pos, axis=1)
        _, w = merged_frame.shape
        x_pos += x_vel
        if x_pos >= w or x_pos <= -w:
            x_pos = x_pos % w
        hemera_term_api.print(merged_frame)
        if trip_randomize == 10:
            tilemap = np.random.randint(1, 16, size=(6, 8), dtype=np.uint8)
            trip_randomize = 0
            component_store.register_entity_component(
                scene_entity, TilemapComponent(tilemap, 32)
            )
        else:
            trip_randomize += 1

        # time.sleep(2)
        # time.sleep(0.5)
        # time.sleep(0.0666)  # 15 fps
        time.sleep(0.0333)  # 30 fps
        # time.sleep(0.0222)  #45 fps
        # time.sleep(0.0167)  # 60 fps
        # time.sleep(0.00833)  # 120 FPS
