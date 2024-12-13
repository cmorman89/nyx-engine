"""
AetherRenderer Frame Rendering Module

This module processes game entities and components in layers before merging those layers into a
final frame that is sent to Hemera for printing to the terminal.

Classes:
    AetherRenderer: The primary orchestrator of entity rendering, respoinsible for generating
        layered subframes and then merging them into a frame to be printed. Needs split up.

Mythology:
    In the Greek pantheon, Aether is the son of Nyx (Night) and Erebus (Darkness). He personifies
    the upper air -- the pure, bright atmosphere breathed by the gods. Aether is also considered the
    ethereal medium through which the divine realm is perceived, representing the luminous,
    untainted essence that fills the heavens.

TODO:
    - Store frame layers as a 3D axis-0 stack of 2d arrays (numpy)

"""

from typing import Dict
from uuid import UUID

import numpy as np

from nyx.aether_renderer.aether_dimensions import AetherDimensions
from nyx.moros_ecs.component.renderable_components import (
    BackgroundColorComponent,
    RenderableComponent,
    TilemapComponent,
)
from nyx.moros_ecs.system.tileset_system import TilemapSystem


class AetherRenderer:
    """

    Attributes:
        term_size_h:
    """

    def __init__(self, window_h: int = 0, window_w: int = 0):
        """Initialize the renderer with constraints on the render window dimensions and placeholder
        dictionaries/frames/ndarrays.

        Args:
            window_h (int, optional): The maximum rendering height. Defaults to 0, a skipped value
            window_w (int, optional): The maximum rendering width. Defaults to 0, a skipped value
        """

        # Rendering window sizes and constraints
        self.dimensions = AetherDimensions(window_h=window_h, window_w=window_w)

        # State-related data
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.background_color_code: int | np.uint8 = 0

        # Entities
        self.current_layer_entities = {}
        self.layered_entities = {}

        # Frames/ndarrays
        self.layered_frames = {}
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
        self.layered_entities = entities
        return self

    def render(self):
        """Main entry point for rendering"""
        self.layered_frames = {}
        if not self.layered_entities:
            raise ValueError("AetherRenderer has no layers to render.")
        self._update_terminal_size()
        self._new_merged_frame()
        self._process_layers()
        self._merge_layers()
        self._apply_bg_color()
        return self.merged_frame

    def _new_merged_frame(self):
        """Create a new merged_frame"""
        self.merged_frame = np.zeros(
            (self.effective_view_h, self.effective_view_w), dtype=np.uint8
        )

    def _process_layers(self):
        """Iterate through each z-index layer and process entities/components by calling a
        handling method."""
        for z_index, entity_dict in self.layered_entities.items():
            self._new_subframe(z_index)
            for component_dict in entity_dict.values():
                for component in component_dict.values():
                    # Store background color in z-index 0 layer for later use.
                    if z_index == 0 and isinstance(component, BackgroundColorComponent):
                        self._process_background_color_component(component)
                    elif isinstance(component, TilemapComponent):
                        self._process_tilemap_component(component)

    def _new_subframe(self, z_index: int = 0):
        """Create a new working frame for each z-index/priority/layer."""
        self.layered_frames[z_index] = np.zeros(
            (self.effective_view_h, self.effective_view_w), dtype=np.uint8
        )

    def _merge_layers(self):
        """Merge each z-index subframe (nparray) into the merged frame (nparray) by working from
        high to low"""
        # Cache values before loop
        subframe_stack = (
            self.layered_frames
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
        tm_sys = TilemapSystem(self.layered_frames[0], self.dimensions)
        tm_sys.process(component)
