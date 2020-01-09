import gbvision as gbv
from gbvision.utils.tracker import Tracker

from constants import CONTOUR_MIN_AREA, SHAPE_LIFESPAN
from .base_algorithm import BaseAlgorithm
from constants.game_objects import POWER_CELL
from constants.thresholds import POWER_CELL_THRESHOLD


def get_closest(shapes, finder):
    tmp = None
    distance = lambda x: gbv.distance_from_object(finder.locations_from_shapes([x])[0])
    for i in shapes:
        if tmp is None:
            tmp = i
        elif distance(i) < distance(tmp):
            tmp = i

    return [tmp]


class FindPowerCells(BaseAlgorithm):
    algorithm_name = 'power cells'

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)

        self.finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=POWER_CELL_THRESHOLD,
                                       contour_min_area=CONTOUR_MIN_AREA)
        self.debug = False
        if self.debug:
            self.window = gbv.FeedWindow('feed', drawing_pipeline=lambda x: (self.finder.find_shapes(x), x) +
                                                                            (lambda x: gbv.draw_circles(frame=x[1],
                                                                                                        circs=x[0],
                                                                                                        color=(
                                                                                                            255, 0, 0)
                                                                                                        )))

        self.continues = None
        self.found_cell = False

        def _process(self, frame: gbv.Frame, camera: gbv.Camera):
            if self.debug:
                self.window.show_frame(frame)

            if not self.found_fuel:
                power_cells = self.finder.find_shapes(frame)
                if len(power_cells) > 0:
                    self.continues = gbv.ContinuesShapeWrapper(finding_pipeline=self.finder, frame=frame,
                                                               shapes=power_cells, shape_type='CIRCLE',
                                                               shape_lifespan=SHAPE_LIFESPAN,
                                                               track_new=True,
                                                               tracker_type=Tracker.TRACKER_TYPE_MEDIANFLOW)
            else:
                power_cells = self.continues.find_shapes(frame)

            closest_location = self.finder.locations_from_shapes(get_closest(power_cells, self.finder), camera)

            return closest_location

    def reset(self, camera: gbv.Camera):
        pass
