import gbvision as gbv
from gbrpi.electronics.led_ring import LedRing

from constants import OUTER_PORT, OUTER_PORT_THRESHOLD, CONTOUR_MIN_AREA
from exceptions.algorithm_incomplete import AlgorithmIncomplete
from .base_algorithm import BaseAlgorithm
from vision_master import LOW_EXPOSURE


class FindHexagon(BaseAlgorithm):
    algorithm_name = 'hexagon'

    def __init__(self, output_key, success_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, success_key, conn, log_algorithm_incomplete)
        self.finder = gbv.ContourFinder(game_object=OUTER_PORT, threshold_func=OUTER_PORT_THRESHOLD,
                                        contour_min_area=CONTOUR_MIN_AREA)
        if self.DEBUG:
            self.stream = None

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        """
        :param frame: frame received from camera
        :param camera: camera used
        :return: location
        """
        if self.DEBUG:
            self.stream.send_frame(frame)
        shapes = self.finder.find_shapes(frame)
        if len(shapes) == 0:
            raise AlgorithmIncomplete()
        hexagon = shapes[0]
        loc = self.finder.locations_from_shapes([hexagon], camera)[0]
        if BaseAlgorithm.DEBUG:
            print(loc)
        return loc

    def reset(self, camera: gbv.Camera, led_ring: LedRing):
        camera.set_auto_exposure(False)
        camera.set_exposure(LOW_EXPOSURE)
        led_ring.on()
        if self.DEBUG:
            self.stream = gbv.TCPStreamBroadcaster(5809)
