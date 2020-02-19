import gbvision as gbv
from constants import *
from algorithms import *
import cv2
from algorithms.find_power_cells import FindPowerCells
import random
import numpy as np


def get_max_dist(pts):
    if len(pts) < 2:
        print("need more points")
        return
    max_dist = np.linalg.norm(np.array(pts[0])-np.array(pts[1]))
    for i in range(1, len(pts)-1):
        max_dist = max(max_dist, np.linalg.norm(np.array(pts[i])-np.array(pts[i+1])))
    return max_dist

def color(p1, p2, max_dist):
    dist = np.linalg.norm(np.array(p2)-np.array(p1))
    color_double = dist/max_dist
    if color_double <= 0.5:
        return 0, 255, color_double * 510
    return 0, 255 - color_double * 510, 255

cam = gbv.USBCamera(0)
cam.set_auto_exposure(False)
cam.set_exposure(-5)
cam.set_fps(999999.0)

win = gbv.FeedWindow("window")
win.open()

thresh = gbv.ColorThreshold([[0, 65], [174, 254], [84, 164]], 'HSV')
finder = gbv.CircleFinder(game_object=POWER_CELL, threshold_func=thresh,
                          contour_min_area=CONTOUR_MIN_AREA, area_scalar=RADIUS_SCALAR, circles_process=gbv.sort_circles + gbv.filter_inner_circles)

pnts = []

while 1:
    _, frame = cam.read()

    cnts = finder.find_shapes(frame)
    if cnts:
        print(cnts[0][0])
        pnts.append(cnts[0][0])
    frame = gbv.draw_circles(frame, cnts, (255, 0, 0), 3)

    win.show_frame(frame)

    if win.last_key_pressed == 'c':
        print('_'*900)
        max_dist = get_max_dist(pnts)
        if pnts:
            for i in range(len(pnts) - 1):
                cv2.line(frame, (int(pnts[i][0]), int(pnts[i][1])), (int(pnts[i+1][0]), int(pnts[i+1][1])), color(pnts[i], pnts[i+1], max_dist), 4)

            while 1:
                win.show_frame(frame)

                if win.last_key_pressed == 'c':
                        break

    if win.last_key_pressed == 'r':
        pnts = []

