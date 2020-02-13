import gbvision as gbv
import numpy as np

from gbrpi.electronics.led_ring import LedRing

from constants import HIGH_EXPOSURE, RADIUS_SCALAR
from constants.continuity import CONTOUR_MIN_AREA, SHAPE_LIFESPAN
from constants.game_objects import POWER_CELL
from constants.thresholds import POWER_CELL_THRESHOLD
from .base_algorithm import BaseAlgorithm


class FindPowerCells(BaseAlgorithm):
    algorithm_name = 'power_cells'

    def __init__(self, output_key, success_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, success_key, conn, log_algorithm_incomplete)

        self.finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=POWER_CELL_THRESHOLD,
                                       contour_min_area=CONTOUR_MIN_AREA, area_scalar=RADIUS_SCALAR)
        self.shaper = self.finder.find_shapes

        self.continues = gbv.ContinuesShapeWrapper(finding_pipeline=self.shaper, frame=None, shapes=[],
                                                   shape_type='CIRCLE', shape_lifespan=SHAPE_LIFESPAN, track_new=True,
                                                   tracker_type='MEDIANFLOW')
        self.found_cell = False
        self.closest_id = None

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        power_cells = self.continues.find_shapes(frame)
        if len(power_cells) == 0:
            raise self.AlgorithmIncomplete()
        if self.closest_id is None or self.closest_id not in power_cells:
            self.closest_id = self.__get_optimal(power_cells, camera)

        loc = self.finder.locations_from_shapes(shapes=[power_cells[self.closest_id]], camera=camera)[0]
        self.logger.debug(loc)
        return loc

    def reset(self, camera: gbv.Camera, led_ring: LedRing):
        camera.set_auto_exposure(False)
        camera.set_exposure(HIGH_EXPOSURE)
        led_ring.off()

    def __get_optimal(self, shapes, camera):
        closest_id = None
        current_cost = -1

        def cost(x):
            location = self.finder.locations_from_shapes([shapes[x]], camera)[0]
            return (10 * abs(gbv.plane_angle_by_location(location)) / (2 * np.pi) + 1) * gbv.plane_distance_from_object(
                location)

        for i in shapes:
            tmp_cost = cost(i)
            if closest_id is None or tmp_cost < current_cost:
                closest_id = i
                current_cost = tmp_cost

        return closest_id
