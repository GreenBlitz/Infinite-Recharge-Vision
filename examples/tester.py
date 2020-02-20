from constants import *
import cv2
import numpy as np
import time
from gbvision import LIFECAM_3000
import matplotlib.pyplot as plt


def get_max_speed(pts, times):
    if len(pts) < 2:
        print("need more points")
        return
    dist = np.linalg.norm(np.array(pts[0])-np.array(pts[1]))
    max_speed = dist/(times[1]-times[0])
    for i in range(1, len(pts)-1):
        max_speed = max(max_speed, np.linalg.norm(np.array(pts[i])-np.array(pts[i+1]))/(times[i+1]-times[i]))
    return max_speed


def color(p1, p2, t1, t2, max_speed):
    speed = np.linalg.norm(np.array(p2)-np.array(p1))/(t2-t1)
    color_double = speed/max_speed
    if color_double <= 0.5:
        return 0, 255, color_double * 510
    return 0, 255 - color_double * 510, 255


cam = gbv.CameraList([gbv.USBCamera(2), gbv.USBCamera(0), gbv.USBCamera(1)])
CAMS = len(cam)

cam.set_auto_exposure(False, foreach=True)
cam.set_exposure(-5, foreach=True)
cam.set_fps(999999.0, foreach=True)
win = []
for i in range(CAMS):
    win.append(gbv.FeedWindow(f"window{i}"))
    win[i].open()

thresh = gbv.ColorThreshold([[20, 30], [59, 219], [98, 255]], 'HLS')

finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=thresh,
                          contour_min_area=CONTOUR_MIN_AREA, area_scalar=RADIUS_SCALAR, circles_process=gbv.sort_circles + gbv.filter_inner_circles)
pnts = []
times = []
for i in range(CAMS):
    pnts.append([])
    times.append([])
frames = [None] * CAMS
cnts = [None] * CAMS

while 1:
    for i in range(CAMS):
        ok, frame = cam[i].read()
        frames[i] = frame
        cnts[i] = (finder.find_shapes(frames[i]))
        frames[i] = gbv.draw_circles(frames[i], cnts[i], (255, 0, 0), 3)
        if cnts[i]:
            pnts[i].append(cnts[i][0][0])
            times[i].append(time.time())
        win[i].show_frame(frames[i])

    """_______________________________________________________________"""

    if any(map(lambda x: x.last_key_pressed == 'c', win)):
        print('_'*900)
        max_speeds = [None] * CAMS
        for i in range(CAMS):
            max_speeds[i] = get_max_speed(pnts[i], times[i])
        if all(pnts):
            for win_num in range(CAMS):
                for i in range(len(pnts[win_num]) - 1):
                    cv2.line(frames[win_num], (int(pnts[win_num][i][0]), int(pnts[win_num][i][1])), (int(pnts[win_num][i+1][0]), int(pnts[win_num][i+1][1])), color(pnts[win_num][i], pnts[win_num][i+1], times[win_num][i], times[win_num][i+1], max_speeds[win_num]), 4)

                plt.subplot(CAMS, 1, 1+win_num)
                plt.scatter([i[0] for i in pnts[win_num]], [-i[1] for i in pnts[win_num]])

            plt.show()

            while 1:
                for win_num in range(CAMS):
                    win[win_num].show_frame(frames[win_num])

                if any(map(lambda x: x.last_key_pressed == 'c', win)):
                    break

    if any(map(lambda x: x.last_key_pressed == 'r', win)):
        print("reset" * 500)
        for win_num in range(CAMS):
            pnts[win_num] = []
            times[win_num] = []


