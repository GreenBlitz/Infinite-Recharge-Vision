import gbvision as gbv

from .base_algorithm import BaseAlgorithm


class FindHexagon(BaseAlgorithm):
    algorithm_name = 'hexagon'

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        pass

    def reset(self):
        pass
