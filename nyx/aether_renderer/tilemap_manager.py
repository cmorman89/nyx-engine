import numpy as np
from nyx.aether_renderer.aether_dimensions import AetherDimensions


class TilemapManager:
    background_color = None
    tilemap_key_array = None
    rendered_tilemap = None
    tilemap_position = (0, 0)
    tile_dimensions = 32
    tileset_textures = {}

    def __init__(self, dimensions: AetherDimensions):
        self.dimensions = dimensions
        self.culled_tilemap_key = None

    def create_tilemap(self, tilemap: np.ndarray):
        TilemapManager.tilemap_key_array = tilemap

    def create_tileset(self, tileset: dict, tile_dimension: int = 32):
        TilemapManager.tileset_textures = tileset
        TilemapManager.tile_dimensions = tile_dimension

    def render_tilemap(self):
        tilemap = TilemapManager.tilemap_key_array
        tile_dimension = TilemapManager.tile_dimensions
        tileset = TilemapManager.tileset_textures
        h, w = tilemap.shape
        rendered_tilemap = np.zeros(
            (h * tile_dimension, w * tile_dimension), dtype=np.uint8
        )
        for y in range(h):
            for x in range(w):
                tile_x_start = x * tile_dimension
                tile_y_start = y * tile_dimension
                tile_x_end = tile_x_start + tile_dimension
                tile_y_end = tile_y_start + tile_dimension
                tile_texture = tileset[tilemap[y, x]]
                rendered_tilemap[tile_y_start:tile_y_end, tile_x_start:tile_x_end] = (
                    tile_texture
                )
        TilemapManager.rendered_tilemap = rendered_tilemap

    # def cull_tilemap_key(self):
    #     tilemap_key = TilemapManager.tilemap_key_array
    #     frame_h, frame_w = (
    #         self.dimensions.effective_y_resolution,
    #         self.dimensions.effective_x_resolution,
    #     )
    #     map_h, map_w = TilemapManager.tilemap_key_array.shape
    #     map_x, map_y = TilemapManager.tilemap_position
    #     tile_d = TilemapManager.tile_dimensions

    #     # Calculate the maximum number of tiles that can be rendered
    #     map_h_max, map_w_max = (
    #         ceil(frame_h / tile_d),
    #         ceil(frame_w / tile_d),
    #     )
    #     # Create the culled tilemap key array of only the visible tiles
    #     # Find the starting point of the tilemap key array
    #     map_y_start = max(0, ceil(map_y / tile_d))
    #     map_x_start = max(0, ceil(map_x / tile_d))
    #     # Find the ending point of the tilemap key array
    #     map_y_end = min(map_h, map_h_max)
    #     map_x_end = min(map_w, map_w_max)
    #     # If the tilemap key array is smaller than the frame, repeat it to fill the frame
    #     if map_h < map_h_max:
    #         TilemapManager.culled_tilemap_key = np.vstack(
    #             (tilemap_key, tilemap_key[: map_h_max - map_h, :])
    #         )
    #     if map_w < map_w_max:
    #         TilemapManager.culled_tilemap_key = np.hstack(
    #             (tilemap_key, tilemap_key[:, : map_w_max - map_w])
    #         )

    # If the tilemap key array is larger than the frame, cut it to fit the frame
    # Check if tilemap needs to be rerenedered by comparing the culled tilemap key to the previous one or if position changed
    # If the tilemap needs to be rerendered, render the tilemap
    #
