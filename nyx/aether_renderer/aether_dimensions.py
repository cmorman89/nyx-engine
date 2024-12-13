from nyx.hemera_term_fx.term_utils import TerminalUtils


class AetherDimensions:
    def __init__(self, window_h: int = 0, window_w: int = 0):
        # Terminal Size
        self.term_size_h: int = 0
        self.term_size_w: int = 0
        # Manual Size Requested
        self.window_h: int = window_h
        self.window_w: int = window_w
        # Actual Render Dimensions
        self.effective_window_h: int = 0
        self.effective_window_w: int = 0

        self._update_terminal_size()

    def _update_terminal_size(self):
        terminal_size = TerminalUtils.get_terminal_dimensions()
        self.term_size_h = (terminal_size.lines - 4) * 2
        self.term_size_w = terminal_size.columns - 2
        self.effective_window_h = (
            min(self.window_h, self.term_size_h)
            if self.window_h > 0
            else self.term_size_h
        )
        self.effective_window_w = (
            min(self.window_w, self.term_size_w)
            if self.window_w > 0
            else self.term_size_w
        )

        if self.effective_window_h % 2 != 0:
            self.effective_window_h -= 1
