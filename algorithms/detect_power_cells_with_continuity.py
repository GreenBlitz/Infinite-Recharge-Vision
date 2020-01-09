import gbvision as gbv
from .base_algorithm import BaseAlgorithm
from constants.game_objects import POWER_CELL
from constants.thresholds import POWER_CELL_THRESHOLD


class FindPowerCells(BaseAlgorithm):

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)

        self.finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=POWER_CELL_THRESHOLD)
        self.debug = False
        if self.debug:
            self.window = gbv.FeedWindow('feed', drawing_pipeline=gbv.EMPTY_PIPELINE + (
            lambda x: (self.finder.find_shapes(x), x)) + (lambda x: (x[0][0], x[1])) + (
                                                                  lambda x: gbv.draw_circles(frame=x[1], circs=x[0],
                                                                                             color=(255, 0, 0))))
        else:
            self.window = gbv.FeedWindow('feed')

        def _process(self, frame: gbv.Frame, camera: gbv.Camera):
            if self.debug:
                self.window.show_frame(frame)

            power_cells = self.finder.find_shapes(frame)
            power_cells_locations = self.finder.locations_from_shapes(power_cells, camera)

            return power_cells_locations[0]

    def reset(self, camera: gbv.Camera):
        pass
