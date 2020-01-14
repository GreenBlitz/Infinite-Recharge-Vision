import gbvision as gbv

from constants import OUTER_PORT, OUTER_PORT_THRESHOLD, CONTOUR_MIN_AREA
from exceptions.algorithm_incomplete import AlgorithmIncomplete
from .base_algorithm import BaseAlgorithm


class FindHexagon(BaseAlgorithm):
    algorithm_name = 'hexagon'

    def __init__(self, output_key, success_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, success_key, conn, log_algorithm_incomplete)
        self.finder = gbv.ContourFinder(game_object=OUTER_PORT, threshold_func=OUTER_PORT_THRESHOLD,
                                        contour_min_area=CONTOUR_MIN_AREA)
        self.window = gbv.FeedWindow('window')

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        """
        :param frame: frame received from camera
        :param camera: camera used
        :return: location
        """
        if BaseAlgorithm.DEBUG:
            self.window.show_frame(frame)
        shapes = self.finder.find_shapes(frame)
        if len(shapes) == 0:
            raise AlgorithmIncomplete()
        hexagon = shapes[0]
        loc = self.finder.locations_from_shapes([hexagon], camera)[0]
        if BaseAlgorithm.DEBUG:
            print(loc)
        return loc

    def reset(self, camera: gbv.Camera):
        camera.set_exposure(10)
