"""
Terminal Utlities Module

This module defines static methods to easily manipulate printing to the terminal. It is mostly for
my own sanity + centralized update location if the underlying logic must change.

Classes:
    TerminalUtils: A collection of static methods to manipulate terminal printing.
"""

import os
from typing import Tuple


class TerminalUtils:
    """A collection of static methods to manipulate terminal printing.

    Methods:
        clear_term(): Clear the terminal display correctly for both Windows- and Unix-based systems.
        reset_format(): Return the ANSI escape sequence to reset the terminal formatting.
        cursor_to_origin(): Return the ANSI escape sequence to move the printing cursor back to the
            first position in the terminal window.
        cursor_rel_move(): Return the ANSI escape sequence to move the printing cursor relatively to
            its current position in the terminal.
        cursor_abs_move(): Return the ANSI escape sequence to move the printing cursor to a specific
            location within the terminal.
        get_terminal_dimensions(): Return the terminal size as a tuple of integers in (h, w) format.
    """

    @staticmethod
    def clear_term():
        """Clear the terminal display correctly for both Windows- and Unix-based systems."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def reset_format() -> str:
        """Return the ANSI escape sequence to reset the terminal formatting.

        Returns:
            str: The ANSI escape sequence to reset the terminal..
        """
        return "\033[0m"

    @staticmethod
    def cursor_to_origin() -> str:
        """Return the ANSI escape sequence to move the printing cursor back to the first position
        in the terminal window.

        Returns:
            str: The ANSI escape sequence to relocate the cursor.
        """
        return "\033[H"

    @staticmethod
    def cursor_rel_move(x: int = 0, y: int = 0) -> str:
        """Return the ANSI escape sequence to move the printing cursor relatively to its current
        position in the terminal.

        Args:
            x (int, optional): Left (- value) or right (+ value) to move the cursor. Defaults to 0.
            y (int, optional): Up( - value) or down (+ value) to move the curosor. Defaults to 0.

        Returns:
            str: The ANSI escape sequence to relocate the cursor.
        """
        commands = []
        if y != 0:
            y_ref = f"{abs(y)}{'A' if y < 0 else 'B'}"
            commands.append(f"\033[{y_ref}")
        if x != 0:
            x_ref = f"{abs(x)}{'C' if x > 0 else 'D'}"
            commands.append(f"\033[{x_ref}")
        return "".join(commands)

    @staticmethod
    def cursor_abs_move(pixel_x: int, pixel_y: int) -> str:
        """Return the ANSI escape sequence to move the printing cursor to a specific location
        within the terminal. Takes zero-based index.

        Args:
            pixel_x (int): the x index of the column.
            pixel_y (int): the y index based on the row.

        Returns:
            str: The ANSI escape sequence to relocate the cursor.
        """
        # Convert zero-based indices to one-based for ANSI
        row = (pixel_y) + 1
        column = pixel_x + 1
        return f"\033[{row};{column}H"

    @staticmethod
    def get_terminal_dimensions() -> Tuple[int, int]:
        """Return the terminal size as a tuple of integers in (h, w) format."""
        terminal_size = os.get_terminal_size()
        return (terminal_size.lines, terminal_size.columns)
