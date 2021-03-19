import gbvision as gbv
from gbrpi.electronics.led_ring import LedRing
from gbvision.models.cameras import LIFECAM_3000
from constants import OUTER_PORT, OUTER_PORT_THRESHOLD, CONTOUR_MIN_AREA, LOW_EXPOSURE
from constants.game_objects import OUTER_PORT
from constants.continuity import CONTOUR_MIN_AREA

ERODE = 11
DILATE_I = 5
DILATE_F = 1


def _process(frame: gbv.Frame, camera: gbv.Camera):
    """
    :param frame: frame received from camera
    :param camera: camera used
    :return: location
    """
    threshold = gbv.ColorThreshold([[30, 110], [215, 255], [70, 150]], 'HSV')
    finder = gbv.CircleFinder(threshold, OUTER_PORT, contour_min_area=CONTOUR_MIN_AREA)
    shapes = finder.find_shapes(frame)
    if len(shapes) == 0:
        return (-1, -1, -1)
    hexagon = shapes[-1]

    loc = finder.locations_from_shapes([hexagon], camera)[0]
    return loc


def reset(camera: gbv.Camera):
    camera.set_auto_exposure(False)
    camera.set_exposure(-10)


def main():
    threshold = gbv.ColorThreshold([[30, 110], [215, 255], [70, 150]], 'HSV')
    camera = gbv.USBCamera(1, LIFECAM_3000)
    reset(camera)

    org = gbv.FeedWindow('Org', drawing_pipeline=threshold)
    window = gbv.FeedWindow('Feed',
                            drawing_pipeline=gbv.DrawCircles(threshold + gbv.Dilate(DILATE_I) + gbv.ErodeAndDilate((ERODE, DILATE_F)),
                                                             (0, 0, 255)))
    thresholdwindow = gbv.FeedWindow('feedthresh',
                                     drawing_pipeline=threshold + gbv.Dilate(DILATE_I) + gbv.ErodeAndDilate((ERODE, DILATE_F)))
    while True:
        ok, frame = camera.read()
        window.show_frame(frame)
        org.show_frame(frame)
        thresholdwindow.show_frame(frame)

        if 'q' == window.last_key_pressed or 'q' == org.last_key_pressed or 'q' == thresholdwindow.last_key_pressed:
            break

        result = _process(frame, camera)
        if -1 not in result:
            print(_process(frame, camera))

    window.close()


if __name__ == '__main__':
    main()
