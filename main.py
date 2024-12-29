from datetime import datetime
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
        "z-index": ZIndexComponent(3),
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


def generate_planet(engine: NyxEngine):
    planet_id = engine.entity_manager.create_entity("planet-sprite").entity_id
    texture = NyxAssetImport.open_asset("alien-planet")
    h, w = texture.shape
    planet_comps = {
        "position": PositionComponent(engine.aether_renderer.dimensions.effective_window_w - 1, 0),
        "dimensions": DimensionsComponent(h, w),
        "z-index": ZIndexComponent(2),
        "velocity": VelocityComponent(-10, 2),
        "texture": TextureComponent(texture=texture),
    }
    for comp_name, comp in planet_comps.items():
        engine.component_manager.add_component(
            entity_id=planet_id, component_name=comp_name, component=comp
        )

    # Set ship components as variables
    velocity: VelocityComponent = engine.component_manager.get_component(
        entity_id=planet_id, component_name="velocity"
    )
    position: PositionComponent = engine.component_manager.get_component(
        entity_id=planet_id, component_name="position"
    )
    dimensions: DimensionsComponent = engine.component_manager.get_component(
        entity_id=planet_id, component_name="dimensions"
    )
    return planet_id, dimensions, position, velocity


if __name__ == "__main__":
    # Configs
    #Line profile string buffer printing:
    line_profiling = False
    # Tilemap
    tilemap_h, tilemap_w = 10, 10
    tile_d = 32
    tile_start, tile_end = 1, 16
    # Dimensions
    window_height = 360
    window_width = 480

    # Start the engine
    engine = NyxEngine()
    engine.hemera_term_fx.run_line_profile = line_profiling
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

    # Create a planet:
    # planet_id, planet_dimensions, planet_position, planet_velocity = generate_planet(
    #     engine
    # )

    # Make the spaceship
    spaceship_id, spaceship_dimensions, spaceship_position, spaceship_velocity = (
        generate_spaceship(engine)
    )
    # Make a laser beam blast
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
        "z-index": ZIndexComponent(4),
        "velocity": VelocityComponent(600, 0),
        "texture": TextureComponent(laser_texture),
    }

    # Start loop
    while True:
        start_time = datetime.now()

        # Spaceship moves up and down
        if spaceship_position.render_y_pos >= (
            engine.aether_renderer.dimensions.effective_window_h
            - spaceship_dimensions.height
        ):
            spaceship_velocity.y_vel = -(abs(spaceship_velocity.y_vel))
        if spaceship_position.render_y_pos <= 1:
            spaceship_velocity.y_vel = abs(spaceship_velocity.y_vel)

        # Random horizontal spaceship drift
        spaceship_velocity.x_vel += randint(-3, 3)
        spaceship_velocity.x_vel = max(-100, min(100, spaceship_velocity.x_vel))
        if spaceship_position.render_x_pos >= 60:
            spaceship_velocity.x_vel = -(abs(spaceship_velocity.x_vel))
        elif spaceship_position.render_x_pos <= 5:
            spaceship_velocity.x_vel = abs(spaceship_velocity.x_vel)

        # Fire lasers randomly
        if fire_counter == fire_interval:
            laser_comps["position"] = PositionComponent(
                spaceship_position.render_x_pos + 10,
                spaceship_position.render_y_pos + (spaceship_velocity.y_vel // 100),
            )
            laser_id = engine.entity_manager.create_entity("laser").entity_id
            for comp_name, comp in laser_comps.items():
                engine.component_manager.add_component(
                    entity_id=laser_id, component_name=comp_name, component=comp
                )
            fire_interval = randint(1, 10)
            fire_counter = 0
        fire_counter += 1

        # Randomize tilemap -or- reposition exisiting tilemap
        if tilemap_interval >= 40:
            tilemap = generate_spacebg_tilemap(
                tilemap_h, tilemap_w, tile_start, tile_end
            )
            tilemap_interval = 0
            tilemap_manager.set_tilemap(tilemap)
        else:
            tilemap_manager.pos_x += 1
        tilemap_interval += 1
        tilemap_manager.render()

        # Loop systems
        engine.trigger_systems()
        # Generate frame
        engine.render_frame()
        # Cull off-screen entities
        engine.kill_entities()
        sleep_time = NyxEngine.sec_per_game_loop - (datetime.now() - start_time).seconds
        time.sleep(sleep_time)


