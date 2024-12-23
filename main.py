from random import randint
import time
from typing import Dict, List

import numpy as np

from nyx.aether_renderer.tilemap_manager import TilemapManager
from nyx.moirai_ecs.component.texture_components import TextureComponent
from nyx.moirai_ecs.component.transform_components import (
    DimensionsComponent,
    PositionComponent,
    VelocityComponent,
    ZIndexComponent,
)
from nyx.moirai_ecs.system.movement_system import MovementSystem
from nyx.nyx_engine.nyx_engine import NyxEngine
from nyx.nyx_engine.utils.nyx_asset_import import NyxAssetImport


def load_tiles(filename: str, start: int, end: int) -> List[np.ndarray]:
    # Generate filenames for .nyx files
    tile_files = [f"{filename}-{i}" for i in range(start, end + 1)]
    # Save them to a temporary dictionary
    tile_imports: Dict[int, np.ndarray] = {}
    for i, filename in enumerate(tile_files):
        tile = NyxAssetImport.open_asset(filename)
        tile_imports[i] = tile
    return tile_imports


def generate_spacebg_tilemap(
    height: int,
    width: int,
    value_start: int,
    value_end: int,
):
    return np.random.randint(
        value_start, value_end, size=(height, width), dtype=np.uint8
    )


def generate_spaceship(engine: NyxEngine):
    spaceship_id = engine.entity_manager.create_entity("spaceship-sprite").entity_id
    spaceship_comps = {
        "position": PositionComponent(10, 0),
        "dimensions": DimensionsComponent(24, 24),
        "z-index": ZIndexComponent(2),
        "velocity": VelocityComponent(0, 100),
        "texture": TextureComponent(texture=NyxAssetImport.open_asset("spaceship")),
    }
    for comp_name, comp in spaceship_comps.items():
        engine.component_manager.add_component(
            entity_id=spaceship_id, component_name=comp_name, component=comp
        )

    # Set ship components as variables
    velocity: VelocityComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="velocity"
    )
    position: PositionComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="position"
    )
    dimensions: DimensionsComponent = engine.component_manager.get_component(
        entity_id=spaceship_id, component_name="dimensions"
    )
    return spaceship_id, dimensions, position, velocity


if __name__ == "__main__":
    # Configs
    # Tilemap
    tilemap_h, tilemap_w = 4, 1
    tile_d = 32
    tile_start, tile_end = 1, 16
    # Dimensions
    window_height = 320
    window_width = 480

    # Start the engine
    engine = NyxEngine()
    # Add required systems to loop
    engine.add_system(MovementSystem())

    # Set rendering window
    engine.aether_renderer.dimensions.window_h = window_height
    engine.aether_renderer.dimensions.window_w = window_width
    engine.aether_renderer.dimensions.update()

    # Create a simple tile map and tiles
    tilemap_manager = engine.tilemap_manager
    # Make tileset
    tile_imports = load_tiles("space-tiles", tile_start, tile_end)
    tilemap_manager.set_tileset(tile_imports, tile_d)
    # Make tilemap
    tilemap = generate_spacebg_tilemap(tilemap_h, tilemap_w, tile_start, tile_end)
    tilemap_manager.set_tilemap(tilemap)
    # Prerender tilemap
    tilemap_manager.render()
    rendered_tilemap = TilemapManager.rendered_tilemap

    # Create a sprite:
    spaceship_id, dimensions, position, velocity = generate_spaceship(engine)

    laserbeam_texture = np.array(
        [160, 160, 160, 160, 160, 160, 160, 160], dtype=np.uint8
    )
    laserbeam_space = np.zeros((18, 8), dtype=np.uint8)
    laser_texture = np.vstack((laserbeam_texture, laserbeam_space, laserbeam_texture))
    tilemap_interval = 10
    fire_interval = 7
    fire_counter = 0
    laser_comps = {
        "position": PositionComponent(30, 4),
        "dimensions": DimensionsComponent(8, 3),
        "z-index": ZIndexComponent(3),
        "velocity": VelocityComponent(600, 0),
        "texture": TextureComponent(laser_texture),
    }
    while True:
        if position.render_y_pos >= (
            engine.aether_renderer.dimensions.effective_window_h - dimensions.height
        ):
            velocity.y_vel = -(abs(velocity.y_vel))
        if position.render_y_pos <= 1:
            velocity.y_vel = abs(velocity.y_vel)

        velocity.x_vel += randint(-3, 3)
        velocity.x_vel = max(-100, min(100, velocity.x_vel))
        if position.render_x_pos >= 60:
            velocity.x_vel = -(abs(velocity.x_vel))
        elif position.render_x_pos <= 5:
            velocity.x_vel = abs(velocity.x_vel)
        if fire_counter == fire_interval:
            laser_comps["position"] = PositionComponent(
                position.render_x_pos + 10,
                position.render_y_pos + (velocity.y_vel // 100),
            )
            laser_id = engine.entity_manager.create_entity("laser").entity_id
            for comp_name, comp in laser_comps.items():
                engine.component_manager.add_component(
                    entity_id=laser_id, component_name=comp_name, component=comp
                )
            fire_interval = randint(1, 10)
            fire_counter = 0
        fire_counter += 1

        if tilemap_interval >= 40:
            tilemap = np.random.randint(
                tile_start, tile_end, size=(tilemap_h, tilemap_w), dtype=np.uint8
            )
            tilemap_interval = 0
            tilemap_manager.set_tilemap(tilemap)
        else:
            # TilemapManager.rendered_tilemap = np.roll(
            #     tilemap_manager.rendered_tilemap, -4, axis=1
            # )
            tilemap_manager.pos_x += 1
        tilemap_interval += 1
        tilemap_manager.render()

        # Loop systems
        engine.trigger_systems()
        # Generate frame
        engine.render_frame()
        # Cull off-screen entities
        engine.kill_entities()
        time.sleep(NyxEngine.sec_per_game_loop)

    #     # time.sleep(2)
    #     # time.sleep(0.5)
    #     # time.sleep(0.0666)  # 15 fps
    #     time.sleep(0.0333)  # 30 fps
    #     # time.sleep(0.0222)  #45 fps
    #     # time.sleep(0.0167)  # 60 fps
    #     # time.sleep(0.00833)  # 120 FPS
