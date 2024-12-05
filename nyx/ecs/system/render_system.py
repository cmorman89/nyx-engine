import os
import numpy as np
from nyx.ecs.component.tile_component import GraphicComponent, TransformComponent
from nyx.ecs.nyx_entity_manager import NyxEntityManager


class RenderSystem:
    def __init__(
        self,
        terminal_width: int = 0,
        terminal_height: int = 0,
        view_width: int = 0,
        view_height: int = 0,
    ):
        """Initialize the rendering system with view and terminal size. The view defaults to the terminal size if not provided."""
        terminal_size = RenderSystem.get_terminal_dimensions()
        self.terminal_width = (
            terminal_width if terminal_width > 0 else terminal_size.columns
        )
        self.terminal_height = (
            terminal_height if terminal_height > 0 else terminal_size.lines
        )
        self.view_width = view_width if view_width > 0 else terminal_width
        self.view_height = view_height if view_height > 0 else terminal_height

    def render(self, entity_manager: NyxEntityManager):
        buffer = np.zeros((self.view_height, self.view_width), dtype=np.uint8)
        RenderSystem.clear_terminal()
        for entity in entity_manager.entities:
            components = entity.get_components()
            transform_comp = components.get("TransformComponent")
            graphic_comp = components.get("GraphicComponent")

            if transform_comp and graphic_comp:
                x, y = transform_comp.x, transform_comp.y
                graphic_array = graphic_comp.graphic

                h, w = graphic_array.shape

                buffer[y : y + h, x : x + w] = graphic_array
            self._draw_buffer(buffer=buffer)

    def _draw_buffer(self, buffer: np.ndarray):
        RenderSystem.cursor_to_origin()
        for row in buffer:
            for color in row:
                print(f"\033[48;5;{color}m \033[0m", end="")
            print()

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
