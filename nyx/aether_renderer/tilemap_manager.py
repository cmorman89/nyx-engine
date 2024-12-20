from math import ceil
import numpy as np
from nyx.aether_renderer.aether_dimensions import AetherDimensions


class TilemapManager:
    background_color = None
    ref_tilemap = None
    rendered_tilemap = None
    tilemap_position = (0, 0)
    tile_dimensions = 32
    tileset_textures = {}

    def __init__(self, dimensions: AetherDimensions):
        self.tile_d = 0
        self.dimensions = dimensions
        self.frame_h, self.frame_w = 0, 0
        self.ref_tiles_h, self.ref_tiles_w = 0, 0
        self.frame_tiles_h, self.frame_tiles_w = 0, 0
        self.pos_x, self.pos_y = 0, 0
        self.ref_pos_x, self.ref_pos_y = 0, 0
        self.rolled_ref_tilemap = None
        self.tile_roll_x, self.tile_roll_y = 0, 0
        self.filled_tilemap = None
        self.rel_pos_x, self.rel_pos_y = 0, 0
        self.rel_pos_end_x, self.rel_pos_end_y = 0, 0

    def render(self):
        self._update_calcs()
        self._resize_ref_array()
        self._fill_ref_tilemap()
        self._cull_rendered_tilemap()

        TilemapManager.rendered_tilemap = self.filled_tilemap

    def _update_calcs(self):
        """Update the instance variable calculations for the tilemap rendering."""
        # Get the tile dimensions
        self.tile_d = TilemapManager.tile_dimensions

        # Get the frame size in pixels
        self.frame_h, self.frame_w = (
            self.dimensions.effective_y_resolution,
            self.dimensions.effective_x_resolution,
        )
        # Convert the frame size to tiles (Ceil because we need the partial tile to end the frame)
        self.frame_tiles_h, self.frame_tiles_w = (
            ceil(self.frame_h / self.tile_d),
            ceil(self.frame_w / self.tile_d),
        )
        # Get the size of the reference tilemap in tiles
        self.ref_tiles_h, self.ref_tiles_w = TilemapManager.ref_tilemap.shape

        # Get the position of the tilemap in pixels
        self.pos_x, self.pos_y = TilemapManager.tilemap_position
        # Convert the position of the tilemap to tiles (Floor because we need the partial tile to start the tilemap)
        self.ref_pos_x, self.ref_pos_y = (
            self.pos_x // self.tile_d,
            self.pos_y // self.tile_d,
        )

        # Calculate the relative position of the tilemap in tiles
        self.tile_roll_x = self.ref_pos_x % self.ref_tiles_w
        self.tile_roll_y = self.ref_pos_y % self.ref_tiles_h

        # Calculate the relative position of the tilemap in pixels
        self.rel_pos_x = self.pos_x % self.frame_w
        self.rel_pos_y = self.pos_y % self.frame_h
        self.rel_pos_end_x = self.rel_pos_x + self.frame_w
        self.rel_pos_end_y = self.rel_pos_y + self.frame_h

    def _resize_ref_array(self):
        # Overall strategy:
        # 1. Roll the reference tilemap array to the current position to prepare for tiling and
        #    slicing.
        # 2. Repeat the rolled tilemap array to exceed the frame size without slicing.
        # 3. Slice the current reference tilemap array to fit the frame, including partial tiles as
        #    whole tiles. This also trims the repeated tilemap array to only the visible tiles.
        # 4. Replace the reference tilemap with the culled tilemap for use in rendering.

        # Check if the tilemap is repositioned
        if self.tile_roll_x != 0 or self.tile_roll_y != 0:
            self._roll_ref_tilemap()
        else:
            self.rolled_ref_tilemap = TilemapManager.ref_tilemap

        # Check if the tilemap is smaller than the frame
        if (
            self.ref_tiles_h < self.frame_tiles_h
            or self.ref_tiles_w < self.frame_tiles_w
        ):
            self._expand_ref_tilemap()

        if (self.ref_tiles_h > self.frame_tiles_h) or (
            self.ref_tiles_w > self.frame_tiles_w
        ):
            self._cull_ref_tilemap()

        # Store the culled tilemap for rendering
        TilemapManager.ref_tilemap = self.rolled_ref_tilemap

    def _roll_ref_tilemap(self):
        # Roll the tilemap array to the current position
        # - Convert rightward position (movement to the right) to leftward roll and vice versa
        # - Convert downward position (movement downward) to upward roll and vice versa
        self.rolled_ref_tilemap = np.roll(
            (TilemapManager.ref_tilemap),
            (-self.tile_roll_y, -self.tile_roll_x),
            axis=(0, 1),
        )

    def _expand_ref_tilemap(self):
        ### Move to new EXPAND method after completion
        # Tile the rolled tilemap array to exceed the frame size
        repeats_x = ceil(self.frame_tiles_w / self.ref_tiles_w)
        repeats_y = ceil(self.frame_tiles_h / self.ref_tiles_h)
        self.rolled_ref_tilemap = np.tile(
            self.rolled_ref_tilemap, (repeats_y, repeats_x)
        )[: self.frame_tiles_h, : self.frame_tiles_w]

    def _cull_ref_tilemap(self):
        ### Move to new CONTRACT method after completion
        # Slice the ref. tilemap array to fit the frame, including partial tiles as whole tiles.
        # - Since the tilemap has been rolled, the top left corner of the tilemap is the correct
        #   starting point for the slice.
        self.rolled_ref_tilemap = self.rolled_ref_tilemap[
            : self.frame_tiles_h, : self.frame_tiles_w
        ]

    def set_tilemap(self, tilemap: np.ndarray):
        TilemapManager.ref_tilemap = tilemap

    def set_tileset(self, tileset: dict, tile_dimension: int = 32):
        TilemapManager.tileset_textures = tileset
        TilemapManager.tile_dimensions = tile_dimension

    def _fill_ref_tilemap(self):
        ref_tilemap = TilemapManager.ref_tilemap
        tile_d = self.tile_d
        tileset = TilemapManager.tileset_textures
        h, w = ref_tilemap.shape

        # Create a new, blank tilemap to render the tileset onto.
        filled_tilemap = np.zeros((h * tile_d, w * tile_d), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                tile_texture = tileset[ref_tilemap[y, x]]
                filled_tilemap[
                    y * tile_d : (y + 1) * tile_d, x * tile_d : (x + 1) * tile_d
                ] = tile_texture

        self.filled_tilemap = filled_tilemap

    def _cull_rendered_tilemap(self):
        self.filled_tilemap = self.filled_tilemap[
            self.rel_pos_y : self.rel_pos_end_y, self.rel_pos_x : self.rel_pos_end_x
        ]
