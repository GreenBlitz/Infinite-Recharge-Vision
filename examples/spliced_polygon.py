import gbvision as gbv
import numpy as np

from constants import OUTER_PORT_TRIANGLE
from constants.distances import OUTER_PORT_WIDTH

thr = gbv.ColorThreshold([[34, 114], [215, 255], [72, 152]], gbv.ColorThreshold.THRESH_TYPE_HSV) + gbv.Erode(
    3) + gbv.Dilate(15)

tri = gbv.GameObject(OUTER_PORT_TRIANGLE)


def find_triangles(cnt):
    if cnt is None:
        return []
    _cnt = cnt
    cnt = cnt.reshape(cnt.size // 2, 2)
    if cnt.size != 12:
        return []
    cnt = sorted(cnt, key=lambda x: x[0])
    cnt = [np.array(cnt[:3]), np.array(cnt[3:])]
    return cnt


def main():
    finder = gbv.PolygonFinder(threshold_func=thr, game_object=tri)
    camera = gbv.AsyncUSBCamera(1)
    camera.wait_start_reading()
    camera.set_exposure(-13)
    func = (thr + gbv.find_contours + gbv.sort_contours + gbv.contours_to_polygons + (
        lambda x: x[0] if len(x) > 0 else None) + find_triangles)
    draw_func = lambda frame: gbv.draw_contours(frame, func(frame), (0, 255, 0), thickness=5)
    thresh_window = gbv.CameraWindow('threshold', camera, drawing_pipeline=thr)
    window = gbv.CameraWindow('feed', camera, drawing_pipeline=func)

    thresh_window.show_async()
    window.show_async()

    while True:
        val = func(camera.read()[1])
        if len(val) != 2:
            continue
        loc1, loc2 = finder.locations_from_shapes(val, camera)
        dis = np.abs(loc1[0] - loc2[0]) + 0.3
        a = -np.arccos(dis / OUTER_PORT_WIDTH)


if __name__ == '__main__':
    main()
