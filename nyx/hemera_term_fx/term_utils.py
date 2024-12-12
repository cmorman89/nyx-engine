import os


class TerminalUtils:
    @staticmethod
    def clear_term():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def set_fg_color():
        pass

    @staticmethod
    def set_bg_color():
        pass

    @staticmethod
    def reset_format():
        return "\033[0m"

    @staticmethod
    def cursor_to_origin():
        return "\033[H"

    @staticmethod
    def cursor_rel_move(x: int = 0, y: int = 0) -> str:
        commands = []
        if y != 0:
            y_ref = f"{abs(y)}{'A' if y < 0 else 'B'}"
            commands.append(f"\033[{y_ref}")
        if x != 0:
            x_ref = f"{abs(x)}{'C' if x > 0 else 'D'}"
            commands.append(f"\033[{x_ref}")
        return "".join(commands)

    @staticmethod
    def cursor_abs_move(row: int, col: int):
        return f"\033[{row};{col}H"

    @staticmethod
    def cursor_subpixel_abs_move(pixel_x: int, sub_pixel_y: int):
        """Account for each character being composed of two stacked pixels.

        Args:
            pixel_x (int): the x index of the pixel coumn
            sub_pixel_y (int): the y index based on the subpixel row

        Returns:
            str: ANSI escape sequence to relocate the cursor.
        """
        # Convert zero-based indices to one-based for ANSI
        row = (sub_pixel_y) + 1
        column = pixel_x + 1
        return f"\033[{row};{column}H"

    @staticmethod
    def get_terminal_dimensions():
        return os.get_terminal_size()
