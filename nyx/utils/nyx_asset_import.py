
import ast
import os

import numpy as np


class NyxAssetImport:
    
    @staticmethod
    def open_asset(file_name: str, file_path: str = None):
        module_path = os.path.dirname(__file__)
        path = os.path.join(module_path, f"../../examples/assets/nyx/{file_name}.nyx")
        with open(path) as file:
            return np.array(ast.literal_eval(file.read()), dtype=np.uint8)

