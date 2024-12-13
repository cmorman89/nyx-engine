"""
View/Window Size Helper Module

This module allows dynamic resizing of the terminal window, while still retaining a fullscreen or
program-overriden window size. This is done without exceeding the terminal bounds, resulting in no
unintended line wraparound.

Classes:
    AetherDimensions: Tracks and updates terminal and window size.
"""

from nyx.hemera_term_fx.term_utils import TerminalUtils


class AetherDimensions:
    """Tracks and updates terminal and window size dynamically.

    Attributes:
        term_size_h: The padded terminal height (in printing characters).
        term_size_w: The padded terminal width (in printing characters).

        window_h: The program-requested window height (in printing characters).
        window_w: The program-requested window width (in printing characters).

        effective_window_h: The final height used by the renderer/program (in printing characters).
        effective_window_w: The final width used by the renderer/program (in printing characters).

    Methods:
        update: Update the dimensions of the rendered frames.
    """

    def __init__(self, window_h: int = 0, window_w: int = 0):
        # Terminal Size
        self.term_size_h: int = 0
        self.term_size_w: int = 0
        # Manual Size Requested
        self.window_h: int = window_h if window_h > 0 and window_w > 0 else 0
        self.window_w: int = window_w if window_w > 0 and window_h > 0 else 0
        # Actual Render Dimensions
        self.effective_window_h: int = 0
        self.effective_window_w: int = 0

        self.update()

    def update(self):
        """Update the dimensions of the rendered frames."""
        self._set_terminal_size()
        self._set_effective_window()
        self._truncate_odd_last_row()

    def _set_terminal_size(self):
        """Pad and store the current terminal size dimensions."""
        terminal_size_y, terminal_size_x = TerminalUtils.get_terminal_dimensions()
        padding_h = 4
        padding_w = 2
        self.term_size_h = (
            terminal_size_y - padding_h
        ) * 2  # 2 pixel rows -> 1 subpixel row
        self.term_size_w = terminal_size_x - padding_w

    def _set_effective_window(self):
        """Set the effective, usable dimensions for the rendered frames based on terminal size and
        program-defined window size.
        """
        # Set the effective window to the program-specified size, up to the padded terminal
        # dimensions. This cutoff is required to prevent lines wrapping around.
        if self._window_is_set():
            self.effective_window_h, self.effective_window_w = (
                min(self.window_h, self.term_size_h),
                min(self.window_w, self.term_size_w),
            )
        # If the window is not set (=0), use the padded terminal dimensions (fullscreen).
        else:
            self.effective_window_h, self.effective_window_w = (
                self.term_size_h,
                self.term_size_w,
            )

    def _truncate_odd_last_row(self):
        """Remove the last line from available dimensions if it is odd (due to subpixel rendering
        requiring grouped pixels -- an odd last row would be missing the paired data).
        """
        if self.effective_window_h % 2 != 0:
            self.effective_window_h -= 1

    def _window_is_set(self) -> bool:
        """Check if the window has been set by the program.

        Returns:
            bool: If the window is manually set.
        """
        return self.window_h > 0 and self.window_w > 0
