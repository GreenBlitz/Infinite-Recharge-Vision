from constants import *
import cv2
import numpy as np
import time
from gbvision import LIFECAM_3000


def get_max_speed(pts, times):
    if len(pts) < 2:
        print("need more points")
        return
    max_speed = np.linalg.norm(np.array(pts[0])-np.array(pts[1]))/(times[1]-times[0])
    for i in range(1, len(pts)-1):
        print(np.linalg.norm(np.array(pts[i])-np.array(pts[i+1]))/(times[i+1]-times[i]))
        max_speed = max(max_speed, np.linalg.norm(np.array(pts[i])-np.array(pts[i+1]))/(times[i+1]-times[i]))
    print("---------------------\n" + str(max_speed))
    return max_speed


def color(p1, p2, t1, t2, max_speed):
    speed = np.linalg.norm(np.array(p2)-np.array(p1))/(t2-t1)
    color_double = speed/max_speed
    if color_double <= 0.5:
        return 0, 255, color_double * 510
    return 0, 255 - color_double * 510, 255


cam = gbv.CameraList([gbv.USBCamera(2), gbv.USBCamera(1)])

cam.set_auto_exposure(False, foreach=True)
cam.set_exposure(-5, foreach=True)
cam.set_fps(999999.0, foreach=True)

win1 = gbv.FeedWindow("window1")
win2 = gbv.FeedWindow("window2")

win1.open()
win2.open()

thresh = gbv.ColorThreshold([[0, 63], [42, 122], [168, 248]], 'HLS')

finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=thresh,
                          contour_min_area=CONTOUR_MIN_AREA, area_scalar=RADIUS_SCALAR, circles_process=gbv.sort_circles + gbv.filter_inner_circles)

pnts1 = []
times1 = []

pnts2 = []
times2 = []

while 1:
    _, frame0 = cam[0].read()
    _, frame1 = cam[1].read()

    cnts1 = finder.find_shapes(frame0)
    cnts2 = finder.find_shapes(frame1)

    frame0 = gbv.draw_circles(frame0, cnts1, (255, 0, 0), 3)
    frame1 = gbv.draw_circles(frame1, cnts2, (255, 0, 0), 3)

    if cnts1:
        # print(cnts[0][0])
        pnts1.append(cnts1[0][0])
        times1.append(time.time())

    if cnts2:
        # print(cnts[0][0])
        pnts2.append(cnts2[0][0])
        times2.append(time.time())

    win1.show_frame(frame0)
    win2.show_frame(frame1)

    """_______________________________________________________________"""

    if win1.last_key_pressed == 'c' or win2.last_key_pressed == 'c':
        print('_'*900)
        max_speed1 = get_max_speed(pnts1, times1)
        max_speed2 = get_max_speed(pnts2, times2)
        if pnts1 and pnts2:
            for i in range(len(pnts1) - 1):
                cv2.line(frame0, (int(pnts1[i][0]), int(pnts1[i][1])), (int(pnts1[i+1][0]), int(pnts1[i+1][1])), color(pnts1[i], pnts1[i+1], times1[i], times1[i+1], max_speed1), 4)

            for i in range(len(pnts2) - 1):
                cv2.line(frame1, (int(pnts2[i][0]), int(pnts2[i][1])), (int(pnts2[i+1][0]), int(pnts2[i+1][1])), color(pnts2[i], pnts2[i+1], times2[i], times2[i+1], max_speed2), 4)

            while 1:
                win1.show_frame(frame0)
                win2.show_frame(frame1)

                if win1.last_key_pressed == 'c' or win2.last_key_pressed == 'c':
                        break

    if win1.last_key_pressed == 'r' or win2.last_key_pressed == 'r':
        pnts1 = []
        times1 = []

        pnts2 = []
        times2 = []
