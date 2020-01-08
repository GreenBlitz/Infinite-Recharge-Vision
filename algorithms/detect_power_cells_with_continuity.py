import gbvision as gbv
from .base_algorithm import BaseAlgorithm
from constants.game_objects import POWER_CELL


class FindPowerCells(BaseAlgorithm):

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(output_key, error_key, conn, log_algorithm_incomplete)

        self.finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=POWER_CELL_THRESHOLD)