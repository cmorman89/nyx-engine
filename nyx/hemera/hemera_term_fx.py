import sys
from typing import Tuple
import numpy as np

from nyx.hemera.term_utils import TerminalUtils


class HemeraTermFx:
    def __init__(self, viewport_h: int = 0, viewport_w: int = 0):
        self._ansi_table = self._precompute_ansi_table()

    def output(self, new_frame: np.ndarray = None):
        self.print_to_term(new_frame)

    def print_to_term(self, new_frame):
        frame = new_frame
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
