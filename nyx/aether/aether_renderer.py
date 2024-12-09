from math import ceil
from typing import Dict
from uuid import UUID

import numpy as np

from nyx.engine.ecs.component.renderable_components import (
    BackgroundColorComponent,
    RenderableComponent,
    TilemapComponent,
)
from nyx.engine.stores.tileset_store import TilesetStore
from nyx.hemera.term_utils import TerminalUtils


class AetherRenderer:
    def __init__(self, viewport_h: int = 0, viewport_w: int = 0):
        terminal_size = TerminalUtils.get_terminal_dimensions()
        self.term_h = terminal_size.lines
        self.term_w = terminal_size.columns // 2
        self.view_h = viewport_h if viewport_h > 0 else self.term_h
        self.view_w = viewport_w if viewport_w > 0 else self.term_w
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.background_color_code = 0
        self.z_indexed_entity_layers = {}
        self.current_layer_entities = {}
        self.z_indexed_working_frames = {}
        self.merged_frame: np.ndarray = self._new_merged_frame()

    def accept_entities(
        self, entities: Dict[int, Dict[UUID, Dict[str, RenderableComponent]]]
    ):
        """Receive and store the list of entities to render from AetherBridgeSystem

        Args:
            entities (Dict[int, Dict[UUID, Dict[str, RenderableComponent]]]): _description_

        Returns:
            _type_: _description_
        """
        self.z_indexed_entity_layers = entities
        return self

    def render(self):
        """Main entry point for rendering"""
        if not self.z_indexed_entity_layers:
            raise ValueError("AetherRenderer has no layers to render.")
        self.z_indexed_working_frames = {}
        self._new_merged_frame()
        self._process_layers()
        self._merge_layers()
        self._apply_bg_color()
        return self.merged_frame

    def _new_merged_frame(self):
        """Create a new merged_frame"""
        self.merged_frame = np.zeros((self.view_h, self.view_w), dtype=np.uint8)

    def _process_layers(self):
        """Iterate through each z-index layer and process entities/components by calling a
        handling method."""
        for z_index, entity_dict in self.z_indexed_entity_layers.items():
            self._new_subframe(z_index)
            for entity_id, component_dict in entity_dict.items():
                for component in component_dict.values():
                    # Store background color in z-index 0 layer for later use.
                    if z_index == 0 and isinstance(component, BackgroundColorComponent):
                        self._process_background_color_component(component)
                    elif isinstance(component, TilemapComponent):
                        self._process_tilemap_component(component)

    def _new_subframe(self, z_index: int = 0):
        """Create a new working frame for each z-index/priority/layer."""
        self.z_indexed_working_frames[z_index] = np.zeros(
            (self.view_h, self.view_w), dtype=np.uint8
        )

    def _merge_layers(self):
        """Merge each z-index subframe (nparray) into the merged frame (nparray) by working from
        high to low"""
        # Cache values before loop
        subframe_stack = (
            self.z_indexed_working_frames
        )  # Dict = {z_index (int), subframe (ndarray)}
        merged_frame = self.merged_frame  # Note: ndarray, uint8

        # Desc. sort the z-index keys, and iterate from the highest priority to the lowest. Each
        # subframe layer replaces pixel information in the merged_frame where the merged_frame cell
        # value = 0.
        for z_index in sorted(subframe_stack, reverse=True):
            merged_frame = np.where(
                merged_frame == 0, subframe_stack[z_index], merged_frame
            )
        self.merged_frame = merged_frame

    def _apply_bg_color(self):
        """Replace any '0' in the nparray/frame with the background color code."""
        merged_frame = self.merged_frame
        merged_frame[merged_frame == 0] = self.background_color_code

    def _process_background_color_component(
        self, bg_component: BackgroundColorComponent
    ):
        """Store the background color for later use."""
        self.background_color_code = bg_component.bg_color_code

    def _process_tilemap_component(self, component: TilemapComponent):
        tilemap = component.tilemap
        textures = TilesetStore.tileset_textures
        map_h, map_w = tilemap.shape
        tile_d = component.tile_dimension
        rendered_map = self.z_indexed_working_frames[
            0
        ]  # Tilemap exclusively occupies layer 0
        # Render 1 tile out of visible in x and y if any of that tile showing in the view.
        # map_w_max = ceil(self.view_w / tile_d)
        # map_h_max = ceil(self.view_h / tile_d)
        # But for now, lets not exceed the bounds:
        map_w_max = self.view_w // tile_d
        map_h_max = self.view_h // tile_d
        for y in range(min(map_h, map_h_max)):
            for x in range(min(map_w, map_w_max)):
                # Get the tile id at location y, x.
                tile_id = tilemap[y, x]
                # Get the texture for that tile ID.
                tile_texture = textures[tile_id]
                # Slice the ndarray from y, x (origin) for d elements in each axis.
                rendered_map[
                    y * tile_d : (y + 1) * tile_d, x * tile_d : (x + 1) * tile_d
                ] = tile_texture
