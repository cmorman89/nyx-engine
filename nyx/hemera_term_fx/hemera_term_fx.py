"""
HemeraTermFx Terminal Printing Module:

This module handles the low-level implementation of the terminal printer given an input frame.

The printing workflow is:

    1. Accept a pre-rendered, complete frame (a 2D np.ndarray, dtype=np.uint8)

    2. Convert to a subpixel representation by slicing even/odd rows and stacking them to form a 3D
       np.ndarray. (Note: a subpixel is a stacked unicode block character "▀", that can be formatted
       with both a foreground and background color to fit two pixels into one printing character.)

    3. Generate a delta framebuffer of only changed pixels by comparing the new subpixel frame to
       the previously-cached last frame (or a blank frame if unavailable or otherwise not usable).

    4. Process the delta framebuffer of subpixels into the printing block characters "▀". Colors are
       issued by ANSI escape sequences. A buffer is held for the last foreground and background
       colors used to prevent excessive ANSI switching. Cursor relocations are similarly issued only
       when a non-contiguous subpixel is encountered.

Classes:
    HemeraTermFx: The primary printing orchestration and processing class. It takes a delta frame-
        buffer and prints it to the terminal.

Mythology:
    In the Greek pantheon, Hemera is the personification of day and light, the daughter of Nyx
    (Night) and Erebus (Darkness). As the embodiment of light she dispels the shadows of night,
    bringing clarity and illumination to creation and all within it.
"""

import sys
import numpy as np

from nyx.hemera_term_fx.term_utils import TerminalUtils


class HemeraTermFx:
    """The primary printing orchestration and processing class. It takes a delta frame-buffer and
    prints it to the terminal.

    Attributes:
        old_subpixel_frame (np.ndarray): The cached last frame rendered, as subpixels.
        clear_term_on_run (bool, optional): Issues a terminal clear command on next render.
            Defaults to False.
    """

    def __init__(self, clear_term_on_run: bool = False):
        """Construct Hemera with an empty frame buffer."""
        self.old_subpixel_frame: np.ndarray = None
        self.clear_term_on_run: bool = clear_term_on_run

    def print(self, new_frame: np.ndarray = None):
        """Print the new frame to the terminal in color and using vertical-stacked subpixels.

        Args:
            new_frame (np.ndarray, optional): Completed frame from `AetherRender`. Defaults to None.
        """

        # 1. Generate subpixel frame from the new frame.
        new_subpixel_frame = self._convert_to_subpixels(new_frame)
        # 2. Compare the subpixel frame to the last subpixel frame to get only what has changed.
        delta_frame = self._calculate_delta_framebuffer(new_subpixel_frame)
        # 3. Print the delta framebuffer to the terminal window.
        self._generate_string_buffer(delta_frame)

    def _convert_to_subpixels(self, new_frame: np.ndarray) -> np.ndarray:
        """Convert the input frame from 2D ndarray -> 3D ndarray of even/odd row pixel colors.

        Args:
            new_frame (np.ndarray, optional): Completed frame from `AetherRender`.

        Returns:
            np.ndarray: The subpixel 3D NumPy array.
        """
        return np.stack([new_frame[::2, :], new_frame[1::2, :]])

    def _calculate_delta_framebuffer(
        self, new_subpixel_frame: np.ndarray
    ) -> np.ndarray:
        """Generate a delta framebuffer consisting of only the changed subpixel-pairs (fg + bg) from
        the last frame generated.

        Args:
            new_subpixel_frame (np.ndarray): The new subpixel frame to compare.

        Returns:
            np.ndarray: The delta framebuffer of only the changed pixels.
        """
        # Generate a blank 3D array in place of the old frame if the old frame does not exists or is
        # of the incorrect dimensions (ie, the terminal has been resized and a full -- not delta --
        # reprint of the new frame is required).
        if (
            self.old_subpixel_frame is None
            or self.old_subpixel_frame.shape != new_subpixel_frame.shape
        ):
            self.old_subpixel_frame = np.zeros(new_subpixel_frame.shape, dtype=np.uint8)

        # Create the delta frame by comparing the new frame to the old frame along the "stacked"
        # axis; retains the changed subpixel color pairs while using the zeroed array as a source
        # to remove unchanged subpixel pairs from the delta framebuffer.
        delta_frame = np.where(
            np.any(
                new_subpixel_frame != self.old_subpixel_frame, axis=0, keepdims=True
            ),
            new_subpixel_frame,
            np.zeros_like(new_subpixel_frame),
        )

        # Cached the new, non-delta subpixel frame as the old subpixel frame for comparision in the
        # next iteration.
        self.old_subpixel_frame = new_subpixel_frame

        return delta_frame

    def _generate_string_buffer(self, delta_frame: np.ndarray):
        """Convert the delta frame to its color-formatted `str` representation form before printing
        to the terminal.

        Args:
            delta_frame (np.ndarray): The delta frame to process and print"""

        run_buffer = ""
        last_ansi_fg_color, last_ansi_bg_color = np.uint8(0), np.uint8(0)
        last_subpixel_pair = (
            np.uint8(0),
            np.uint8(0),
        )
        _, h, w = delta_frame.shape

        # Iterate the subpixel delta frame using a 2D index
        for y, x in np.ndindex(h, w):
            # Save each axis-0 colors to a tuple
            fg_color, bg_color = subpixel_pair = tuple(delta_frame[:, y, x])

            # Check if subpixel is printable (not (0, 0))
            if subpixel_pair != (np.uint8(0), np.uint8(0)):
                # Issue a cursor relocate and flush the run buffer if the last subpixel pair was
                # non-printing (0, 0)
                if last_subpixel_pair == (np.uint8(0), np.uint8(0)):
                    sys.stdout.write(run_buffer)
                    run_buffer = TerminalUtils.cursor_abs_move(x, y)

                # Issue color format sequences only when a new color is needed
                if fg_color != last_ansi_fg_color:
                    run_buffer += f"\033[38;5;{fg_color}m"
                if bg_color != last_ansi_bg_color:
                    run_buffer += f"\033[48;5;{bg_color}m"
                # Add the printing character
                run_buffer += "▀"

            # Add new line at the end of each row
            if x == w - 1:
                run_buffer += "\n"

            # Cache the color values
            last_subpixel_pair = subpixel_pair

        # Flush the final buffer and stdout after frame processing
        sys.stdout.write(run_buffer)
        sys.stdout.flush()

        # Reset the run buffer
        run_buffer = ""
