"""
Render System Module

Rendering system to take a GraphicalComponent and print it to the terminal.

Note:
    - Chars to use: [ █ , ▀ , ▄ ]
    - This will likely split into the basic rendering system that then feeds into the larger terminal graphics rendering api
    -   FPS  Target Processing Time per Frame (ms)
        1                             1000.00
        5                               200.00
        10                             100.00
        15                               66.66
        30                               33.33
"""

import os
import sys
from typing import Tuple


import numpy as np
from nyx.engine.ecs.nyx_entity_manager import NyxEntityManager
from nyx.engine.ecs.system.nyx_system_base import NyxSystem


class RenderSystem(NyxSystem):
    def __init__(
        self,
        ecs: NyxEntityManager,
        terminal_width: int = 0,
        terminal_height: int = 0,
        view_width: int = 0,
        view_height: int = 0,
    ):
        """Initialize the rendering system with view and terminal size. The view defaults to the terminal size if not provided."""

        super().__init__(ecs)
        terminal_size = RenderSystem.get_terminal_dimensions()
        self.terminal_width = (
            terminal_width if terminal_width > 0 else terminal_size.columns
        )
        self.terminal_height = (
            terminal_height if terminal_height > 0 else terminal_size.lines
        )
        self.view_width = view_width if view_width > 0 else self.terminal_width
        self.view_height = view_height if view_height > 0 else self.terminal_height
        self._ansi_table: np.ndarray = self._precompute_ansi_table()

    def render(self, clear_term: bool = True):
        """Render the entity to the terminal."""
        entity_manager = self.ecs
        buffer = np.zeros((self.view_height, self.view_width), dtype=np.uint8)
        self._initialize_terminal(clear_term=clear_term)
        for entity in entity_manager.entities:
            components = entity.get_components()
            transform_comp = components.get("TransformComponent")
            graphic_comp = components.get("GraphicComponent")

            if transform_comp and graphic_comp:
                x, y = transform_comp.x, transform_comp.y
                graphic_array = np.repeat(graphic_comp.graphic_arr, 3, axis=1)

                h, w = graphic_array.shape

                buffer[y : y + h, x : x + w] = graphic_array
            self._preframe_actions()
            self._draw_buffer(buffer=buffer)

    def _draw_buffer(self, buffer: np.ndarray):
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

    def _initialize_terminal(self, clear_term: bool = True):
        self._ansi_table = (
            self._precompute_ansi_table()
            if self._ansi_table is not None
            else self._ansi_table
        )
        if clear_term:
            RenderSystem.clear_terminal()

    def _preframe_actions(self):
        RenderSystem.cursor_to_origin()

    def _precompute_ansi_table(self, low_high_vals: Tuple[int, int] = (0, 255)):
        ansi_range = range(low_high_vals[0], low_high_vals[1] + 1)
        return np.array(
            [f"\033[38;5;{color}m█" if color > 0 else " " for color in ansi_range],
            dtype="<U20",
        )

    @staticmethod
    def reset_terminal_formatting():
        return "\033[0m"

    @staticmethod
    def get_terminal_dimensions():
        return os.get_terminal_size()

    @staticmethod
    def clear_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def cursor_to_origin():
        print("\033[H", end="")

    @staticmethod
    def move_cursor(row: int, col: int):
        # ANSI escape sequence to move the cursor to the given row and column
        print(f"\033[{row};{col}H", end="")