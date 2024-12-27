import io
import sys
from line_profiler import LineProfiler
import numpy as np

from nyx.hemera_term_fx.term_utils import TerminalUtils


class HemeraTermFx:
    """The primary printing orchestration and processing class. It takes a delta frame-buffer and
    prints it to the terminal.

    Attributes:
        old_subpixel_frame (np.ndarray): The cached last frame rendered, as subpixels.
        clear_term_on_run (bool, optional): Issues a terminal clear command on next render.
            Defaults to False.
        buffer_log (str): A log of the buffer for debugging purposes.
    """

    def __init__(
        self,
        clear_term_on_run: bool = False,
        # profile_output_file="line_profile_output.txt",
    ):
        """Construct Hemera with an empty frame buffer."""
        self.old_subpixel_frame: np.ndarray = None
        self.clear_term_on_run: bool = clear_term_on_run
    #     self.profile_output_file = profile_output_file
    #     self.profiler = LineProfiler()

    #     # Profile the _generate_string_buffer method
    #     self.profiler.add_function(self._generate_string_buffer)

    # def _redirect_print_to_profiler(self, *args, **kwargs):
    #     """Redirect print output to profiler's file output."""
    #     with open(self.profile_output_file, "a") as f:
    #         self.profiler.print_stats(stream=f)

    def print(self, new_frame: np.ndarray = None):
        """Print the new frame to the terminal in color and using vertical-stacked subpixels.

        Args:
            new_frame (np.ndarray, optional): Completed frame from AetherRender. Defaults to None.
        """
        # 1. Generate subpixel frame from the new frame.
        new_subpixel_frame = self._convert_to_subpixels(new_frame)
        # 2. Compare the subpixel frame to the last subpixel frame to get only what has changed.
        delta_frame = self._calculate_delta_framebuffer(new_subpixel_frame)

        # Start profiling the process of printing the frame
        # self.profiler.enable_by_count()
        self._generate_string_buffer(delta_frame)
        # self.profiler.disable_by_count()  

        # Log profiler stats into the output file
        # self._redirect_print_to_profiler()


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


    def write_to_term(self, run_buffer):
        sys.stdout.write(run_buffer)

    def flush_to_term(self):
        sys.stdout.flush()

    def sum_bg(self, delta_frame):
        delta_frame[1] = delta_frame[0] + delta_frame[1]
        return delta_frame
    
    def _generate_string_buffer(self, delta_frame: np.ndarray):
        """Convert the delta frame to its color-formatted `str` representation form before printing
        to the terminal.
        Args:
            delta_frame (np.ndarray): The delta frame to process and print.
        """
        # Calculate sum of fg + bg
        delta_frame = self.sum_bg(delta_frame)
        # Calculate the sum of each row
        row_sums = np.sum(delta_frame[1], axis=1)
        # Start the string buffer
        buffer = io.StringIO()
        # Initialize loop variables outside the loop
        last_ansi_fg_color, last_ansi_bg_color = np.uint8(0), np.uint8(0)
        last_subpixel_sum = np.uint8(0)
        empty_pixel = np.uint8(0)
        _, h, w = delta_frame.shape
        fg_color, bg_color = np.uint8(0), np.uint8(0)
        row_buffer = []

        # Iterate frame
        for y in range(h):
            row_buffer = []

            # Check if row has changes
            if row_sums[y] > 0:
                for x in range(w):
                    sum_color = delta_frame[1, y, x]

                    # If the current pixel is printable, get the fg color and calculate the bg color
                    if sum_color != empty_pixel:
                        fg_color = delta_frame[0, y, x]
                        bg_color = sum_color - fg_color

                        # Skip cursor movement if it's the same row/column as the last printed pixel
                        if last_subpixel_sum == empty_pixel:
                            row_buffer.append(TerminalUtils.cursor_abs_move(x, y))

                        # Only write color change sequences when necessary (skip if same as last)
                        # Foreground color check/caching
                        if fg_color != last_ansi_fg_color:
                            row_buffer.append(f"\033[38;5;{fg_color}m")
                            last_ansi_fg_color = fg_color
                        # Background color check/caching
                        if bg_color != last_ansi_bg_color:
                            row_buffer.append(f"\033[48;5;{bg_color}m")
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
