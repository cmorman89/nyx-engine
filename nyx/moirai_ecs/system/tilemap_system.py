# """
# Tilemap System Module

# This module processes tilemap components by replacing the array of reference tile IDs in the
# tilemap with the matching tile texture, while ensuring that terminal and window size constraints
# are respected.
# """

# from math import ceil

# import numpy as np
# from nyx.aether_renderer.aether_renderer import AetherDimensions
# from nyx.moirai_ecs.component.scene_components import TilemapComponent
# from nyx.moirai_ecs.system.base_systems import BaseSystem
# from nyx.nyx_engine.nyx_engine import NyxEngine
# from nyx.nyx_engine.stores.tileset_store import TilesetStore


# class TilemapSystem(BaseSystem):
#     """Processes the tilemap reference IDs to create the rendered tilemap.

#     Attributes:
#         subframe (np.ndarray): The subframe to write the rendered tilemap to.
#         dimensions (AetherDimensions): The class holding current rendering dimension data.
#     """

#     def __init__(self):
#         """Initialize the tilemap system with a subframe to write to and the current render size.

#         Args:
#             subframe (np.ndarray): The subframe to write the rendered tilemap to.
#             dimensions (AetherDimensions): The class holding current rendering dimension data.
#         """
#         self.subframe: np.ndarray = NyxEngine.aether_renderer.layered_frames[0]
#         self.dimensions: AetherDimensions = NyxEngine.aether_renderer.dimensions
#         self.tilemap: TilemapComponent = None

#     def update(self):
#         """Replace the tilemap references with the 2D ndarray tile textures without exceeding the
#         terminal or window bounds.

#         Args:
#             component (TilemapComponent): The component holding the tilemap.
#         """
#         # Tilemap exclusively occupies layer 0
#         rendered_map = self.subframe
#         textures = TilesetStore.tileset_textures
#         tilemap = component.tilemap

#         # Culling Method:
#         #   Extend rendering to frame bounds (but not exceeding)
#         #   - Slices the frame/rendered map to match the current tile
#         #   - AND slices the tile if it will exceed frame bounds

#         # Get window size
#         effective_view_h, effective_view_w = (
#             self.dimensions.effective_window_h,
#             self.dimensions.effective_window_w,
#         )

#         # Set/calculate tilemap bounds; `ceil` ensure even partially exposed tiles are included.
#         tile_d = component.tile_dimension
#         map_h, map_w = tilemap.shape
#         map_h_max, map_w_max = (
#             ceil(effective_view_h / tile_d),
#             ceil(effective_view_w / tile_d),
#         )

#         # Ignore tilemap array values that would be outside the render window
#         for y in range(min(map_h, map_h_max)):
#             for x in range(min(map_w, map_w_max)):
#                 # Get the tile id of the current array element (located index)
#                 tile_id = tilemap[y, x]

#                 # Get the texture for that tile ID.
#                 tile_texture = textures[tile_id]

#                 # Ensure no frame OOB violations
#                 tile_x_start = x * tile_d
#                 tile_x_end = min((x + 1) * tile_d, effective_view_w)
#                 tile_w = tile_x_end - tile_x_start

#                 tile_y_start = y * tile_d
#                 tile_y_end = min((y + 1) * tile_d, effective_view_h)
#                 tile_h = tile_y_end - tile_y_start

#                 # Slice the frame to match the tile size
#                 rendered_map[tile_y_start:tile_y_end, tile_x_start:tile_x_end] = (
#                     tile_texture[0:tile_h, 0:tile_w]
#                 )
