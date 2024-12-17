from random import randint
import time
from typing import Dict, Text
import numpy as np
from nyx.hemera_term_fx.term_utils import TerminalUtils
from nyx.moirai_ecs.component.texture_components import TextureComponent
from nyx.moirai_ecs.component.transform_components import (
    DimensionsComponent,
    PositionComponent,
    VelocityComponent,
    ZIndexComponent,
)
from nyx.moirai_ecs.system.movement_system import MovementSystem
from nyx.nyx_engine.nyx_engine import NyxEngine
from nyx.moirai_ecs.system.aether_bridge_system import AetherBridgeSystem
from nyx.nyx_engine.stores.tileset_store import TilesetStore
from nyx.utils.nyx_asset_import import NyxAssetImport


if __name__ == "__main__":
    engine = NyxEngine()
    # Load Early Managers, Stores, Assets, Systems
    engine.add_system(MovementSystem())

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

    # Create a sprite:
    spaceship_id = engine.entity_manager.create_entity("spaceship-sprite").entity_id
    spaceship_comps = {
        "position": PositionComponent(10, 0),
        "dimensions": DimensionsComponent(24, 24),
        "z-index": ZIndexComponent(2),
        "velocity": VelocityComponent(0, 200),
        "texture": TextureComponent(texture=NyxAssetImport.open_asset("spaceship")),
    }
    for comp_name, comp in spaceship_comps.items():
        engine.component_manager.add_component(
            entity_id=spaceship_id, component_name=comp_name, component=comp
        )
    engine.aether_renderer.dimensions.window_h = 150
    engine.aether_renderer.dimensions.window_w = 275
    engine.aether_renderer.dimensions.update()

    velocity: VelocityComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="velocity"
    )
    position: PositionComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="position"
    )
    dimensions: DimensionsComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="dimensions"
    )
    fire_interval = 7
    fire_counter = 0
    laser_comps = {
        "position": PositionComponent(30, 4),
        "dimensions": DimensionsComponent(4, 1),
        "z-index": ZIndexComponent(3),
        "velocity": VelocityComponent(400, 0),
        "texture": TextureComponent(np.array([[160, 160, 160, 160]], dtype=np.uint8)),
    }
    while True:
        if position.render_y_pos >= (
            engine.aether_renderer.dimensions.window_h - dimensions.height
        ):
            velocity.y_vel = -(abs(velocity.y_vel))
        if position.render_y_pos <= 1:
            velocity.y_vel = abs(velocity.y_vel)
        if fire_counter == fire_interval:
            laser_comps["position"] = PositionComponent(30, position.render_y_pos + 4)
            laser_id = engine.entity_manager.create_entity("laser").entity_id
            for comp_name, comp in laser_comps.items():
                engine.component_manager.add_component(
                    entity_id=laser_id, component_name=comp_name, component=comp
                )
            fire_interval = randint(1, 10)
            fire_counter = 0
        fire_counter += 1
        engine.trigger_systems()
        engine.render_frame()
        engine.kill_entities()
        time.sleep(NyxEngine.sec_per_game_loop)
    # engine.run_game()

    # # Clear the terminal before the first run
    # TerminalUtils.clear_term()
    # # Scrolfel left -> right = positive value
    # # SCroll right -> left = negative value
    # x_pos = 0
    # x_vel = -4
    # trip_randomize = 0
    # # Loop to regenerate colors
    # tilemap = np.random.randint(1, 16, size=(10, 20), dtype=np.uint8)
    # # Create "LevelRoot" Entity
    # scene_entity = entity_manager.create_entity("scene-1")

    # # Add components to entity
    # (
    #     component_store.register_entity_component(
    #         scene_entity, SceneComponent("demo-map")
    #     )
    #     .register_entity_component(scene_entity, ZIndexComponent(0))
    #     # .register_entity_component(scene_entity, BackgroundColorComponent(33))
    #     .register_entity_component(scene_entity, BackgroundColorComponent(16))
    #     .register_entity_component(
    #         scene_entity, TilemapComponent(tilemap, tile_dimension=tile_dimension)
    #     )
    # )
    # while True:
    #     # Call the render system to collect entities and pass to Aether
    #     z_indexed_entities = aether_collector.update()

    #     aether_renderer.dimensions.window_h = 180
    #     aether_renderer.dimensions.window_w = 240
    #     merged_frame = aether_renderer.accept_entities(
    #         aether_collector.update()
    #     ).render()
    #     merged_frame = np.roll(merged_frame, x_pos, axis=1)
    #     _, w = merged_frame.shape
    #     x_pos += x_vel
    #     if x_pos >= w or x_pos <= -w:
    #         x_pos = x_pos % w
    #     hemera_term_api.print(merged_frame)
    #     if trip_randomize == 10:
    #         tilemap = np.random.randint(1, 16, size=(6, 8), dtype=np.uint8)
    #         trip_randomize = 0
    #         component_store.register_entity_component(
    #             scene_entity, TilemapComponent(tilemap, 32)
    #         )
    #     else:
    #         trip_randomize += 1

    #     # time.sleep(2)
    #     # time.sleep(0.5)
    #     # time.sleep(0.0666)  # 15 fps
    #     time.sleep(0.0333)  # 30 fps
    #     # time.sleep(0.0222)  #45 fps
    #     # time.sleep(0.0167)  # 60 fps
    #     # time.sleep(0.00833)  # 120 FPS
