import sys
import numpy as np

from nyx.hemera.term_utils import TerminalUtils


class HemeraTermFx:
    def __init__(self, clear_term_on_run: bool = False):
        self._ansi_table = self._precompute_ansi_table()
        self.old_frame = None
        self.clear_term_on_run = clear_term_on_run

    def output(self, new_frame: np.ndarray = None):
        self.print_subpixel_to_term(self.generate_delta_framebuffer(new_frame))
        # self.print_to_term(new_frame)
        # self.print_subpixel_to_term(new_frame)

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
        sys.stdout.write(
            TerminalUtils.cursor_to_origin()
            + "".join(rasterized_buffer.ravel())
            + "\033[0m"
        )
        sys.stdout.flush()

    def print_subpixel_to_term(self, new_frame):
        buffer = f"{TerminalUtils.cursor_to_origin()}"
        w, h = new_frame.shape
        for y, pixel_row in enumerate(new_frame):
            if y % 2 == 0:
                next_pixel_row_index = y + 1
                if next_pixel_row_index < h:
                    next_pixel_row = new_frame[next_pixel_row_index]
                    for x, fg_color in enumerate(pixel_row):
                        bg_color = next_pixel_row[x]
                        # print(f"fg={fg_color}, bg={bg_color}")
                        buffer += f"\033[38;5;{fg_color};48;5;{bg_color}m▀"
                else:
                    for color in pixel_row:
                        # print(f"fg={color}")
                        buffer += f"\033[38;5;{fg_color}m▀"
                buffer += "\n"

        print(buffer + TerminalUtils.reset_format())

    def _precompute_ansi_table(self):
        ansi_range = range(0, 256)
        return np.array(
            [f"\033[38;5;{color}m██" if color > 0 else "  " for color in ansi_range],
            dtype="<U20",
        )

    def generate_delta_framebuffer(self, new_frame):
        # Generate a new, blank historical frame if one does not exist or term dimensions change.
        # This will force a redraw of the whole scene
        if self.old_frame is None or self.old_frame.shape != new_frame.shape:
            self.old_frame = np.zeros(new_frame.shape, dtype=np.uint8)

        # Create the delta framebuffer by:
        # - Compare the new frame to the old frame
        # - Keep the changed pixels, and set the rest to 0.
        # - "0" represents an *unchanged* pixel that does not need to be redrawn.
        delta_framebuffer = np.where(new_frame != self.old_frame, new_frame, 0)
        self.old_frame = new_frame
        return delta_framebuffer
