import sys
from typing import Tuple
import numpy as np

from nyx.engine.ecs.component.renderable_components import BackgroundColorComponent
from nyx.hemera.term_utils import TerminalUtils


class HemeraRenderer:
    def __init__(self, viewport_h: int = 0, viewport_w: int = 0):
        terminal_size = TerminalUtils.get_terminal_dimensions()
        self.term_h = terminal_size.lines
        self.term_w = terminal_size.columns // 2
        self.view_h = viewport_h if viewport_h > 0 else self.term_h
        self.view_w = viewport_w if viewport_w > 0 else self.term_w
        self.bg_color = 33
        self.working_frame: np.ndarray
        self.generate_working_frame()
        self._ansi_table = self._precompute_ansi_table()

    def render(self, buffer: np.ndarray = None):
        self.generate_working_frame()
        self.draw_working_frame()
        print(
            f"Term Size: ({self.term_w}, {self.term_h}); View Size: ({self.view_w}, {self.view_h})"
        )

    def draw_working_frame(self):
        frame = self.working_frame
        self._fill_bg_color()
        # Generate an empty array of correct dtype and one extra column.
        row, cols = frame.shape
        rasterized_buffer = np.empty((row, cols + 1), dtype=">U20")
        # Fill the new column with new line chars.
        rasterized_buffer[:, -1] = "\n"
        # Map buffer of ints to pre-generated, ANSI-formatted strings.
        rasterized_buffer[:, :-1] = self._ansi_table[frame]
        # Write to the terminal.
        sys.stdout.write("".join(rasterized_buffer.ravel()) + "\033[0m")
        sys.stdout.flush()

    def _precompute_ansi_table(self):
        ansi_range = range(0, 255)
        return np.array(
            [f"\033[38;5;{color}m██" if color > 0 else "  " for color in ansi_range],
            dtype="<U20",
        )

    def _fill_bg_color(self):
        self.working_frame[self.working_frame == 0] = self.bg_color

    def generate_working_frame(self):
        self.working_frame = np.zeros((self.view_h, self.view_w), dtype=np.uint8)

    def _precompute_ansi_table(self, low_high_vals: Tuple[int, int] = (0, 255)):
        ansi_range = range(low_high_vals[0], low_high_vals[1] + 1)
        return np.array(
            [f"\033[38;5;{color}m██" if color > 0 else "  " for color in ansi_range],
            dtype="<U20",
        )
