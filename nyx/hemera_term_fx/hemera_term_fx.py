"""
HemeraTermFx Module

This module contains the HemeraTermFx class, which is responsible for rendering the final frame
to the terminal. It takes a frame from AetherRender and prints it to the terminal in color and
using vertical-stacked subpixels.

It operates by comparing the new frame to the last frame rendered and only printing the changed
subpixel pairs. It also caches the last frame rendered to compare against the new frame.

The overall goal of this class is to reduce the number of terminal writes and cursor movements to
the absolute minimum required to render the frame, enabling high-speed rendering of frames to the
terminal.

Classes:
    HemeraTermFx: The primary printing orchestration and processing class.
"""

from datetime import datetime
import io
import sys
from typing import Dict
from line_profiler import LineProfiler
import numpy as np
from nyx.hemera_term_fx import hemera_cython


class HemeraTermFx:
    """The primary printing orchestration and processing class. It takes a ndarray frame and
    prints it to the terminal.

    Attributes:
        old_subpixel_frame (np.ndarray): The cached last frame rendered, as subpixels.
        clear_term_on_run (bool, optional): Issues a terminal clear command on next render.
            Defaults to False.
        ansi_fg (Dict[np.uint8, str]): A dictionary of ANSI escape codes for foreground colors.
        ansi_bg (Dict[np.uint16, str]): A dictionary of ANSI escape codes for background colors.
        run_line_profile (bool): Whether to run the line profiler on `_generate_string_buffer`
        profiler (LineProfiler): The line profiler object.
        profile_output_file (str): The file to output the line profiler stats to.

    """

    def __init__(self, clear_term_on_run: bool = False):
        """Constructs Hemera with a default subpixel frame and filled ANSI color maps.

        Args:
            clear_term_on_run (bool, optional): Issues a terminal clear command on next render.
                Defaults to False.
        """
        self.old_subpixel_frame: np.ndarray = None
        self.clear_term_on_run: bool = clear_term_on_run

        # Generate ANSI color maps
        self.ansi_fg = self._generate_fg_ansi_map()
        self.ansi_bg = self._generate_bg_ansi_map()

        # Profile the _generate_string_buffer method
        self.run_line_profile = False
        self.profiler = LineProfiler()
        self.profile_output_file = f"{str(datetime.now())}--line_profile_output.txt"
        self.profiler.add_function(self._generate_string_buffer)

    def _generate_fg_ansi_map(self) -> Dict[np.uint8, str]:
        """Generate a dictionary of ANSI escape codes for foreground colors.

        Returns:
            Dict[np.uint8, str]: The ANSI escape codes for foreground colors.
        """
        fg_ansi = {}
        for i in range(256):
            fg_ansi[np.uint8(i)] = f"\033[38;5;{i}m"
        return fg_ansi

    def _generate_bg_ansi_map(self) -> Dict[np.uint16, str]:
        """Generate a dictionary of ANSI escape codes for background colors.

        Returns:
            Dict[np.uint16, str]: The ANSI escape codes for background colors.
        """
        bg_ansi = {}
        for i in range(256):
            bg_ansi[np.uint16(i)] = f"\033[48;5;{i}m"
        return bg_ansi

    def _redirect_print_to_profiler(self, *args, **kwargs):
        """Redirect print output to profiler's file output."""
        with open(self.profile_output_file, "a") as f:
            self.profiler.print_stats(stream=f)

    def print(self, new_frame: np.ndarray = None):
        """Print the new frame to the terminal in color and using vertical-stacked subpixels.

        Args:
            new_frame (np.ndarray, optional): Completed frame from AetherRender. Defaults to None.
        """
        # # 1. Generate subpixel frame from the new frame.
        # new_subpixel_frame = self._convert_to_subpixels(new_frame)
        # # 2. Compare the subpixel frame to the last subpixel frame to get only what has changed.
        # delta_frame = self._calculate_delta_framebuffer(new_subpixel_frame)

        # # Start profiling the process of printing the frame
        # if self.run_line_profile:
        #     self._profile_generate_string_buffer(delta_frame)
        # else:
        #     self._generate_string_buffer(delta_frame)
        hemera_cython._c_hemera_print(new_frame)

    def _profile_generate_string_buffer(self, delta_frame: np.ndarray):
        """Profile the `_generate_string_buffer` method.

        Args:
            delta_frame (np.ndarray): The delta frame to profile.
        """
        self.profiler.enable_by_count()
        self._generate_string_buffer(delta_frame)
        self.profiler.disable_by_count()
        # Log profiler stats into the output file
        self._redirect_print_to_profiler()

    def _convert_to_subpixels(self, new_frame: np.ndarray) -> np.ndarray:
        """Convert the input frame from 2D ndarray -> 3D ndarray of even/odd row pixel colors.

        Args:
            new_frame (np.ndarray, optional): Completed frame from AetherRender.

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

    def write_to_term(self, str_buffer: str):
        """Write the str buffer to the terminal.

        Args:
            str_buffer (str): The string buffer to print to the terminal.
        """
        sys.stdout.write(str_buffer)

    def flush_to_term(self):
        """Flush the terminal output."""
        sys.stdout.flush()

    def sum_bg(self, delta_frame: np.ndarray):
        """Sum the fg and bg colors to get the sum of the fg and bg colors for each pixel. Then,
        return the fg-only delta_frame and the sum_frame.

        Args:
            delta_frame (np.ndarray): The delta frame to process.

        Returns:
            np.ndarray: The fg-only delta frame.
            np.ndarray: The sum frame.

        TODO: Incorporate this function into the subpixel frame generation process to reduce the
            number of times the frame is processed and the number of intermediate arrays created.
        """
        return delta_frame[0], delta_frame[0].astype(np.uint16) + delta_frame[1].astype(
            np.uint16
        )

    def _generate_string_buffer(self, delta_frame: np.ndarray):
        """Convert the delta frame to its color-formatted `str` representation form before printing
        to the terminal.
        Args:
            delta_frame (np.ndarray): The delta frame to process and print.
        """
        # Calculate sum of fg + bg
        delta_frame, sum_frame = self.sum_bg(delta_frame)
        # Calculate the sum of each row
        row_sums = np.sum(sum_frame, axis=1)
        # Start the string buffer
        buffer = io.StringIO()
        # Initialize loop variables outside the loop
        empty_pixel = np.uint8(0)
        empty_sum = np.uint16(0)
        fg_color, bg_color = empty_pixel, empty_sum
        last_ansi_fg_color, last_ansi_bg_color = empty_pixel, empty_sum
        sum_color, last_subpixel_sum = empty_sum, empty_sum
        h, w = delta_frame.shape
        row_buffer = []
        ansi_fg = self.ansi_fg
        ansi_bg = self.ansi_bg

        # Iterate frame
        for y in range(h):
            row_buffer.clear()

            # Check if row has changes
            if row_sums[y] > empty_sum:
                for x in range(w):
                    sum_color = sum_frame[y, x]

                    # If the current pixel is printable, get the fg color and calculate the bg color
                    if sum_color != empty_sum:
                        fg_color = delta_frame[y, x]
                        bg_color = sum_color - fg_color
                        # bg_color = delta_frame[1, y, x]

                        # Skip cursor movement if it's the same row/column as the last printed pixel
                        if last_subpixel_sum == empty_sum:
                            row_buffer.append(f"\033[{y + 1};{x + 1}H")

                        # Only write color change sequences when necessary (skip if same as last)
                        # Foreground color check/caching
                        if fg_color != last_ansi_fg_color:
                            row_buffer.append(ansi_fg[fg_color])
                            last_ansi_fg_color = fg_color
                        # Background color check/caching
                        if bg_color != last_ansi_bg_color:
                            row_buffer.append(ansi_bg[bg_color])
                            last_ansi_bg_color = bg_color

                        # Add the printed character
                        row_buffer.append("▀")

                    # Cache the last sum
                    last_subpixel_sum = sum_color

                # Add the row buffer for the changed row
                buffer.write("".join(row_buffer) + "\n")

        # Output the accumulated buffer to stdout
        self.write_to_term(buffer.getvalue())
        self.flush_to_term()
