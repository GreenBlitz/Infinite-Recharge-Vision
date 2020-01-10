import gbvision as gbv
import cv2

from constants import OUTER_PORT, OUTER_PORT_THRESHOLD, CONTOUR_MIN_AREA
from exceptions.algorithm_incomplete import AlgorithmIncomplete
from .base_algorithm import BaseAlgorithm


class FindHexagon(BaseAlgorithm):
    algorithm_name = 'hexagon'

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)
        self.finder = gbv.ContourFinder(game_object=OUTER_PORT, threshold_func=OUTER_PORT_THRESHOLD,
                                        contour_min_area=200)
        self.debug = True
        self.window = gbv.FeedWindow('window')

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        """

        :param frame: frame recieved from camera
        :param camera: camera used
        :return: location and angle in reference to hexagon
        """
        if self.debug:
            k = self.window.last_key_pressed
            if k != 'q':
                self.window.show_frame(frame)
            else:
                cv2.destroyAllWindows()
        shapes = self.finder.find_shapes(frame)
        if len(shapes) == 0:
            raise AlgorithmIncomplete()
        hexagon = shapes[0]
        loc = self.finder.locations_from_shapes([hexagon], camera)[0]
        if self.debug:
            print(loc)
        return loc

    def reset(self, camera: gbv.Camera):
        camera.set_exposure(-10)
