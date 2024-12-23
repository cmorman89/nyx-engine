"""
Tilemap Manager Module

This module holds the assets needed for a tilemap (textures, reference array, relative position) and
uses that information to construct the rendered tilemap for the frame.

Classes:
    TilemapManager: Manages the rendering of a tilemap onto a frame.
"""

from math import ceil
import numpy as np
from nyx.aether_renderer.aether_dimensions import AetherDimensions


class TilemapManager:
    """Manages the rendering of a tilemap onto a frame by applying the tileset textures to the
    reference tilemap and then culling the rendered tilemap to fit the frame.

    Attributes:
        background_color: The color code for the background of the tilemap.
        ref_tilemap: The reference tilemap array.
        rendered_tilemap: The rendered tilemap array.
        tilemap_position: The position of the tilemap in the frame.
        tile_dimensions: The dimensions of the tiles in pixels.
        tileset_textures: The textures for the tiles in the tileset.
        tile_d: The dimensions of the tiles in pixels.
        dimensions: The dimensions of the frame in pixels.
        frame_h: The height of the frame in pixels.
        frame_w: The width of the frame in pixels.
        ref_tiles_h: The height of the reference tilemap in tiles.
        ref_tiles_w: The width of the reference tilemap in tiles.
        frame_tiles_h: The height of the frame in tiles.
        frame_tiles_w: The width of the frame in tiles.
        pos_x: The x-coordinate of the tilemap in pixels.
        pos_y: The y-coordinate of the tilemap in pixels.
        ref_pos_x: The x-coordinate of the tilemap in tiles.
        ref_pos_y: The y-coordinate of the tilemap in tiles.
        rolled_ref_tilemap: The reference tilemap array rolled to the current position.
        tile_roll_x: The relative x-coordinate of the tilemap in tiles.
        tile_roll_y: The relative y-coordinate of the tilemap in tiles.
        filled_tilemap: The reference tilemap array filled with the tileset textures.
        rel_pos_x: The relative x-coordinate of the tilemap in pixels.
        rel_pos_y: The relative y-coordinate of the tilemap in pixels.
        rel_pos_end_x: The relative end x-coordinate of the tilemap in pixels.
        rel_pos_end_y: The relative end y-coordinate of the tilemap in pixels.

    Methods:
        render: Render the tilemap onto the frame.
        set_tilemap: Set the reference tilemap array.
        set_tileset: Set the tileset textures for the tilemap.
        _upll_ref_tilemap: Slice the ref. tilemap array to fit the frame.
    """

    background_color = None
    ref_tilemap = None
    rendered_tilemap = None
    tilemap_position = (0, 0)
    tile_dimensions = 32
    tileset_textures = {}

    def __init__(self, dimensions: AetherDimensions):
        """Initialize the tilemap manager with the frame dimensions and placeholder variables.

        Args:
            dimensions (AetherDimensions): The dimensions of the frame.
        """
        # Placeholder variables
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
        """Render the tilemap onto the frame."""
        self._update_calcs()
        self._resize_ref_array()
        self._fill_ref_tilemap()
        self._roll_rendered_tilemap()
        self._cull_rendered_tilemap()

        TilemapManager.rendered_tilemap = self.filled_tilemap

    def set_tilemap(self, tilemap: np.ndarray):
        """Set the reference tilemap array.

        Args:
            tilemap (np.ndarray): The reference tilemap array.
        """
        TilemapManager.ref_tilemap = tilemap

    def set_tileset(self, tileset: dict, tile_dimension: int = 32):
        """Set the tileset textures for the tilemap.

        Args:
            tileset (dict): The textures for the tiles in the tileset.
            tile_dimension (int, optional): The dimensions of the tiles in pixels. Defaults to 32.
        """
        TilemapManager.tileset_textures = tileset
        TilemapManager.tile_dimensions = tile_dimension

    def _update_calcs(self):
        """Update the instance variable calculations for the tilemap rendering."""
        # Get the tile dimensions
        self.tile_d = TilemapManager.tile_dimensions

        # Get the frame size in pixels
        self.frame_h, self.frame_w = (
            self.dimensions.effective_window_h,
            self.dimensions.effective_window_w,
        )
        # Convert the frame size to tiles (Ceil because we need the partial tile to end the frame)
        self.frame_tiles_h, self.frame_tiles_w = (
            ceil(self.frame_h / self.tile_d),
            ceil(self.frame_w / self.tile_d),
        )
        # Get the size of the reference tilemap in tiles
        self.ref_tiles_h, self.ref_tiles_w = TilemapManager.ref_tilemap.shape

        # Convert the position of the tilemap to tiles (Floor because we need the partial tile to start the tilemap)
        self.ref_pos_x, self.ref_pos_y = (
            self.pos_x // self.tile_d,
            self.pos_y // self.tile_d,
        )

        # Calculate the relative position of the reference tilemap in tiles
        self.tile_roll_x = self.ref_pos_x % self.ref_tiles_w
        self.tile_roll_y = self.ref_pos_y % self.ref_tiles_h

        # Calculate the relative position of the filled tilemap in pixels
        self.rel_pos_x = self.pos_x % self.frame_w
        self.rel_pos_y = self.pos_y % self.frame_h

    def _resize_ref_array(self):
        """Resize the reference tilemap array to fit the frame."""
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
        """Roll the reference tilemap array to the current position."""
        # - Convert rightward position (movement to the right) to leftward roll and vice versa
        # - Convert downward position (movement downward) to upward roll and vice versa
        self.rolled_ref_tilemap = np.roll(
            (TilemapManager.ref_tilemap),
            (-self.tile_roll_y, -self.tile_roll_x),
            axis=(0, 1),
        )

    def _expand_ref_tilemap(self):
        """Tile the rolled tilemap array to exceed the frame size."""
        repeats_x = ceil(self.frame_tiles_w / self.ref_tiles_w)
        repeats_y = ceil(self.frame_tiles_h / self.ref_tiles_h)
        self.rolled_ref_tilemap = np.tile(
            self.rolled_ref_tilemap, (repeats_y, repeats_x)
        )[: self.frame_tiles_h, : self.frame_tiles_w]

    def _cull_ref_tilemap(self):
        """Slice the reference tilemap array to fit the frame, iluding partial tiles as whole tiles.

        Note: Since the tilemap has been rolled, the top left corner of the tilemap is the correct
            starting point for the slice.
        """
        self.rolled_ref_tilemap = self.rolled_ref_tilemap[
            : self.frame_tiles_h, : self.frame_tiles_w
        ]

    def _fill_ref_tilemap(self):
        """Fill the reference tilemap with the tileset textures."""
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

    def _roll_rendered_tilemap(self):
        """Roll the rendered tilemap to the current position."""
        self.filled_tilemap = np.roll(
            self.filled_tilemap, (-self.rel_pos_y, -self.rel_pos_x), axis=(0, 1)
        )

    def _cull_rendered_tilemap(self):
        """Slice the rendered tilemap to fit the frame."""
        self.filled_tilemap = self.filled_tilemap[: self.frame_h, : self.frame_w]
