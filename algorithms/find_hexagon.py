import gbvision as gbv
from gbvision.finders.polygon_finder import PolygonFinder

from constants import OUTER_PORT, OUTER_PORT_THRESHOLD
from exceptions.algorithm_incomplete import AlgorithmIncomplete
from .base_algorithm import BaseAlgorithm


class FindHexagon(BaseAlgorithm):
    algorithm_name = 'hexagon'

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)
        self.finder = PolygonFinder(game_object=OUTER_PORT, threshold_func=OUTER_PORT_THRESHOLD)

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        """

        :param frame: frame recieved from camera
        :param camera: camera used
        :return: location and angle in reference to hexagon
        """
        shapes = self.finder.find_shapes(frame)
        hex = shapes[0]
        if len(hex) != 6:
            raise AlgorithmIncomplete

        loc = self.finder.locations_from_shapes([hex], camera)[0]

        # TODO add absolute angle
        return loc


    def reset(self, camera: gbv.Camera):
        camera.set_exposure(-10)
