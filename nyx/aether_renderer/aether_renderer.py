"""
AetherRenderer Frame Rendering Module

This module processes game entities and components in layers before merging those layers into a
final frame that is sent to Hemera for printing to the terminal.

Classes:
    AetherRenderer: The primary orchestrator of entity rendering, respoinsible for generating
        layered subframes and then merging them into a frame to be printed. 

Mythology:
    In the Greek pantheon, Aether is the son of Nyx (Night) and Erebus (Darkness). He personifies
    the upper air -- the pure, bright atmosphere breathed by the gods. Aether is also considered the
    ethereal medium through which the divine realm is perceived, representing the luminous,
    untainted essence that fills the heavens.
"""

from typing import Dict, List, Tuple

import numpy as np

from nyx.aether_renderer.aether_dimensions import AetherDimensions


class AetherRenderer:
    """Primary orchestrator of entity rendering, responsible for generating layered subframes and
    then merging them into a frame to be printed.

    Attributes:
        dimensions (AetherDimensions): The constraints on the render window dimensions.
        current_layer_entities (Dict[int, Dict[int, Dict[str, NyxComponent]]]): The entities
            currently being processed.
        layered_entities (Dict[int, List[Tuple[int, int, np.ndarray]]]): The entities to render.
        layered_frames (Dict[int, np.ndarray]): The subframes for each z-index layer.
        merged_frame (np.ndarray): The final merged frame to be printed.

    Methods:
        accept_entities: Receive and store the list of entities to render from AetherBridgeSystem.
        render: Trigger a render of the current entities list held by Aether.
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

        # Entities
        self.current_layer_entities = {}
        self.layered_entities = {}

        # Frames/ndarrays
        self.layered_frames = {}
        self.merged_frame: np.ndarray = self._new_merged_frame()

        # Background color
        self.background_color_code = 0

    def accept_entities(self, entities: Dict[int, List[Tuple[int, int, np.ndarray]]]):
        """Receive and store the list of entities to render from AetherBridgeSystem

        Args:
            entities (Dict[int, List[Tuple[int, int, np.ndarray]]]): The entities to render.
        """
        self.layered_entities = entities
        return self

    def render(self) -> np.ndarray:
        """Trigger a render of the current entities list held by Aether.

        Returns:
            np.ndarray: The merged, 2D frame with uint8 datatype.
        """
        self.layered_frames = {}
        if not self.layered_entities:
            raise ValueError("AetherRenderer has no layers to render.")
        self.dimensions.update()
        self._new_merged_frame()
        self._process_tilemap_component()
        self._process_layers()
        self._merge_layers()
        self._apply_bg_color()
        return self.merged_frame

    def _new_merged_frame(self):
        """Create a new/blank merged frame (2D ndarray) of the correct dimensions for the z-index
        layers to collapse into.
        """
        self.merged_frame = np.zeros(
            (
                self.dimensions.effective_window_h,
                self.dimensions.effective_window_w,
            ),
            dtype=np.uint8,
        )

    def _process_layers(self):
        """Iterate through each z-index layer and process entities/components by calling a specific
        system from the MorosECS and directing them to the appropriate subframe to write to.
        """
        for z_index, entity_list in self.layered_entities.items():
            self._new_subframe(z_index)
            for entity in entity_list:
                # Get frame/dimensions
                frame_w = self.dimensions.effective_window_w
                frame_h = self.dimensions.effective_window_h
                subframe = self.layered_frames[z_index]
                # Get texture
                x, y, texture = entity
                h, w = texture.shape
                # Limit w and h to fit within the frame boundaries
                w = min(w, frame_w - x)
                h = min(h, frame_h - y)
                # Insert texture into subframe
                if w > 0 and h > 0:
                    subframe[y : y + h, x : x + w] = texture[:h, :w]

    def _new_subframe(self, z_index: int = 0):
        """Create a new/blank 2D ndarray for each z-index/priority/layer and insert that subframe
        into the subframe dict with its z-indice as the key value.
        """
        self.layered_frames[z_index] = np.zeros(
            (
                self.dimensions.effective_window_h,
                self.dimensions.effective_window_w,
            ),
            dtype=np.uint8,
        )

    def _merge_layers(self):
        """Merge each z-index subframe (2D ndarray) into the merged frame (2D ndarray) by filling
        transparencies (np.uint8(0)) while iterating the z-indices from high to low.
        """
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

        # Update the instance's reference to the new ndarray (due to np.where creating a new frame)
        self.merged_frame = merged_frame

    def _apply_bg_color(self):
        """Replace any '0' in the final, merged 2D ndarray/frame with the stored background ansi
        color code (unless it is already zero).
        """
        if self.background_color_code != 0:
            self.merged_frame[self.merged_frame == 0] = self.background_color_code

    def _process_tilemap_component(self):
        """Process a `TilemapComponent` by its associated `MorosSystem`.

        Args:
            component (TilemapComponent): The component holding a tilemap array.
        """
        from nyx.nyx_engine.nyx_engine import NyxEngine
        engine = NyxEngine()
        frame_w = self.dimensions.effective_window_w
        frame_h = self.dimensions.effective_window_h

        self.layered_frames[0] = engine.tilemap_manager.rendered_tilemap[
            :frame_h, :frame_w
        ]
