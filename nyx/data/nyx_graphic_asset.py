import numpy as nd

from nyx.data.graphic_asset_base import ProcessedGraphicAsset


class NyxGraphicAsset(ProcessedGraphicAsset):
    def __init__(self, payload: nd.ndarray):
        self.payload: nd.ndarray = payload
