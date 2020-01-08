import gbvision as gbv
import numpy as np
from constants.distances import OUTER_PORT_WIDTH

THRESHOLD = gbv.ColorThreshold([[0, 167], [155, 255], [58, 138]], 'HSV') + gbv.MedianBlur(3) + gbv.Dilate(2)
GREEN = (0, 255, 0)
HALF_TARGET = gbv.GameObject(0.1832007096056126)
finder = gbv.ContourFinder(THRESHOLD, HALF_TARGET)
camera = gbv.AsyncUSBCamera(1, gbv.LIFECAM_3000)


def angle_by_locations(loc1: gbv.Location, loc2: gbv.Location):
    return np.arcsin(max(-1, min(1, (loc1[2] - loc2[2]) / OUTER_PORT_WIDTH)))


@gbv.PipeLine
def contours_process(cnts):
    if len(cnts) != 1:
        return cnts
    cnt = cnts[0].reshape(cnts[0].size // 2, 2)
    center = gbv.contour_center(cnt)

    left, right = gbv.split_list(lambda x: x[0] <= center[0], cnt)
    if len(left) == 0:
        return [np.array(right)]
    if len(right) == 0:
        return [np.array(left)]
    print(
        [gbv.distance_from_object(x) for x in finder.locations_from_shapes([np.array(left), np.array(right)], camera)],
        'angle:\t', angle_by_locations(*finder.locations_from_shapes([np.array(left), np.array(right)], camera)))
    return [np.array(left), np.array(right)]


def main():
    camera.wait_start_reading()
    camera.set_exposure(-10)
    feed = gbv.CameraWindow('feed', camera,
                            drawing_pipeline=gbv.DrawContours(THRESHOLD, GREEN, contours_process=contours_process))
    feed.show_async()
    threshold_window = gbv.CameraWindow('threshold', camera, drawing_pipeline=THRESHOLD)
    threshold_window.show()


if __name__ == '__main__':
    main()
