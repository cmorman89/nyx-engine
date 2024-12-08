import sys
from typing import Tuple
import numpy as np
from nyx.engine.ecs.component.nyx_component import TilemapComponent
from nyx.engine.ecs.system.render_system import AetherBridgeSystem
from nyx.engine.tileset_resource import TilesetResource


class TilemapRenderer:
    def __init__(self, tileset_resource: TilesetResource, tile_dimension: int = 16):
        self.tileset: TilesetResource = tileset_resource
        self.tile_dimension: int = tile_dimension
        self._ansi_table = self._precompute_ansi_table((0, 255))
        self.frame = None
        self.current_offset = 0
        self.view_width = 0
        self.bg_color = None

    def render(self, tilemap_component: TilemapComponent):
        h, w = tilemap_component.tilemap_arr.shape
        d = self.tile_dimension
        self.bg_color = tilemap_component.tilemap_bg
        self.frame = np.zeros((h * d, w * d), dtype=np.int8)
        self.view_width = w * d

        for y in range(h):
            for x in range(w):
                # Get the tile id at location y, x.
                tile_id = tilemap_component.tilemap_arr[y, x]
                # Get the texture for that tile ID.
                tile_texture = self.tileset.tileset_textures[tile_id]
                # Slice the ndarray from y, x (origin) for d elements in each axis.
                self.frame[y * d : (y + 1) * d, x * d : (x + 1) * d] = tile_texture

        AetherBridgeSystem.cursor_to_origin()
        self._draw_buffer(self.frame)

    def scroll(self, shift: int):
        self.current_offset = (self.current_offset + shift) % self.frame.shape[1]

    def render_frame(self):
        AetherBridgeSystem.cursor_to_origin()
        # Slice the visible part of the frame
        visible_frame = self.frame[
            :, self.current_offset : self.current_offset + self.view_width
        ]
        # Handle wraparound if necessary
        if visible_frame.shape[1] < self.view_width:
            wraparound_width = self.view_width - visible_frame.shape[1]
            visible_frame = np.hstack((visible_frame, self.frame[:, :wraparound_width]))
        self._draw_buffer(visible_frame)

    def _draw_buffer(self, buffer: np.ndarray):
        self._fill_bg_color(buffer)
        # Generate an empty array of correct dtype and one extra column.
        row, cols = buffer.shape
        rasterized_buffer = np.empty((row, cols + 1), dtype=">U20")
        # Fill the new column with new line chars.
        rasterized_buffer[:, -1] = "\n"
        # Map buffer of ints to pre-generated, ANSI-formatted strings.
        rasterized_buffer[:, :-1] = self._ansi_table[buffer]
        # Write to the terminal.
        sys.stdout.write("".join(rasterized_buffer.ravel()) + "\033[0m\n")
        sys.stdout.flush()

    def _precompute_ansi_table(self, low_high_vals: Tuple[int, int] = (0, 255)):
        ansi_range = range(low_high_vals[0], low_high_vals[1] + 1)
        return np.array(
            [f"\033[38;5;{color}m██" if color > 0 else "  " for color in ansi_range],
            dtype="<U20",
        )

    def _fill_bg_color(self, buffer):
        if self.bg_color:
            buffer[buffer == 0] = self.bg_color
