from pprint import pprint
import shutil
import sys
import numpy as np

from nyx.hemera.term_utils import TerminalUtils


class HemeraTermFx:
    def __init__(self, clear_term_on_run: bool = False):
        self.old_frame = None
        self.old_subpixel_frame = None
        self.clear_term_on_run = clear_term_on_run

    def output(self, new_frame: np.ndarray = None):
        new_subpixel_frame = self.convert_to_subpixels(new_frame)
        # print(new_subpixel_frame)
        delta_frame = self.calculate_delta_framebuffer(new_subpixel_frame)
        self.generate_string_buffer(delta_frame)

    def convert_to_subpixels(self, new_frame: np.ndarray):
        """Convert the input frame from 2D ndarray -> 3D ndarray of even/odd row pixel colors."""
        return np.stack([new_frame[::2, :], new_frame[1::2, :]])

    def calculate_delta_framebuffer(self, new_subpixel_frame: np.ndarray):
        """Determine which subpixel *groups* change. If either subpixel changes, BOTH subpixels must
        be written to the buffer."""

        if (
            self.old_subpixel_frame is None
            or self.old_subpixel_frame.shape != new_subpixel_frame.shape
        ):
            self.old_subpixel_frame = np.zeros(new_subpixel_frame.shape, dtype=np.uint8)

        delta_frame = np.where(
            np.any(
                new_subpixel_frame != self.old_subpixel_frame, axis=0, keepdims=True
            ),
            new_subpixel_frame,
            np.zeros_like(new_subpixel_frame),
        )
        self.old_subpixel_frame = new_subpixel_frame
        return delta_frame

    def generate_string_buffer(self, delta_frame: np.ndarray):
        """Convert the delta frame to its strings representation form"""
        run_buffer = ""
        last_ansi_fg_color, last_ansi_bg_color = np.uint8(0), np.uint8(0)
        last_subpixel_pair = np.uint8(0), np.uint8(0),
        d, h, w = delta_frame.shape
        # Index the delta frame for position data
        for y, x in np.ndindex(h, w):
            # Save the colors to a tuple
            subpixel_pair = tuple(delta_frame[:, y, x])

            fg_color, bg_color = subpixel_pair
            # Check if subpixel is printable (not (0, 0))
            if subpixel_pair != (np.uint8(0), np.uint8(0)):
                # Issue a cursor relocate if the last subpixel pair was non-printing (0, 0)
                if last_subpixel_pair == (np.uint8(0), np.uint8(0)):
                    sys.stdout.write(run_buffer)  # Write the last run buffer
                    run_buffer = ""  # Start new run buffer upon relocate
                    run_buffer += TerminalUtils.cursor_subpixel_abs_move(x, y)
                # Issue color format changes
                if fg_color != last_ansi_fg_color:
                    run_buffer += f"\033[38;5;{fg_color}m"
                    last_ansi_fg_color = fg_color  # Cache value
                if bg_color != last_ansi_bg_color:
                    run_buffer += f"\033[48;5;{bg_color}m"
                    last_ansi_bg_color = bg_color  # Cache value
                # Add the printing character
                run_buffer += "▀"
            # Add new line at the end of each row
            if x == w - 1:
                run_buffer += "\n"
            last_subpixel_pair = subpixel_pair  # Cache value

        # Print to the terminal
        sys.stdout.write(run_buffer)  # Flush the run buffer after frame
        run_buffer = ""  # Start new run buffer upon new frame
        sys.stdout.flush()  # Print stdout to the terminal
