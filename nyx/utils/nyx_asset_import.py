"""
Asset Impport Module

Basic importer of .nyx files for use in NyxEngine. Needs significant hardening but works for quick
demoes.
"""

import ast
import os

import numpy as np


class NyxAssetImport:
    """Basic importer of .nyx files for use in NyxEngine. Needs significant hardening but works for quick
    demoes.
    """

    @staticmethod
    def open_asset(file_name: str, file_path: str = None):
        """Static method for checking if a file exists before opening to conver the stored array to
        an np.ndarray used in the program."""
        module_path = os.path.dirname(__file__)
        path = os.path.join(module_path, f"../../examples/assets/nyx/{file_name}.nyx")
        with open(path) as file:
            return np.array(ast.literal_eval(file.read()), dtype=np.uint8)
