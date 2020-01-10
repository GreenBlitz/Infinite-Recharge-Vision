import gbvision as gbv

from constants import CONTOUR_MIN_AREA, SHAPE_LIFESPAN
from constants.game_objects import POWER_CELL
from constants.thresholds import POWER_CELL_THRESHOLD
from .base_algorithm import BaseAlgorithm


def get_closest(shapes, finder):
    closest_id = None
    distance = lambda x: gbv.distance_from_object(finder.locations_from_shapes([shapes[x]])[0])
    for i in shapes:
        if closest_id is None or distance(i) < distance(closest_id):
            closest_id = i

    return closest_id


class FindPowerCells(BaseAlgorithm):
    algorithm_name = 'power cells'

    def __init__(self, output_key, error_key, conn, log_algorithm_incomplete=False):
        BaseAlgorithm.__init__(self, output_key, error_key, conn, log_algorithm_incomplete)

        self.finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=POWER_CELL_THRESHOLD,
                                       contour_min_area=CONTOUR_MIN_AREA)
        self.debug = True
        if self.debug:
            self.window = gbv.FeedWindow('feed', drawing_pipeline=
            lambda x: (self.finder.find_shapes(x), x) + (
                lambda x: gbv.draw_circles(frame=x[1], circs=x[0], color=(255, 0, 0))))

        self.continues = gbv.ContinuesShapeWrapper(finding_pipeline=self.finder, frame=None, shapes=[],
                                                   shape_type='CIRCLE', shape_lifespan=SHAPE_LIFESPAN, track_new=True,
                                                   tracker_type='MEDIANFLOW')
        self.found_cell = False
        self.closest_id = -1

    def _process(self, frame: gbv.Frame, camera: gbv.Camera):
        power_cells = self.continues.find_shapes(frame)
        if (self.closest_id == -1 and len(power_cells) > 0) or not power_cells.__contains__(self.closest_id):
            self.closest_id = get_closest(power_cells, self.finder)

        if self.debug:
            not_closest = self.continues.get_shapes_as_list()
            not_closest.remove(power_cells[self.closest_id])
            marked = gbv.PipeLine(lambda x: gbv.draw_circles(circs=not_closest, frame=x, color=(255, 0, 0)) + (
                lambda x: gbv.draw_circles(circs=power_cells[self.closest_id], color=(0, 0, 255), frame=x)))(frame)
            self.window.show_frame(marked)

    def reset(self, camera: gbv.Camera):
        pass
