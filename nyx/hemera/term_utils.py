import os
from re import A


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
    def get_terminal_dimensions():
        return os.get_terminal_size()
