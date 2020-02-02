import math

import gbvision as gbv

import constants

'''
this vision script was created to calibrate denoising of a threshod function for game objects
it finds the best constants for the erode and dilate denoising function in the bounds of 0 - 10
'''

# insert constants in the following variables:
THRESHOLD = None  # the threshold function used to detect the object
GAME_OBJECT = None  # the game object object of the wanted game object
CAMERA = None  # the camera used to detect the object
DISTANCE_FROM_OBJECT = 0


def calculate_distance(erode: int, dilate: int, frame: gbv.Frame):
    thr = THRESHOLD + gbv.Erode(erode) + gbv.Dilate(dilate)
    frame = thr(frame)
    finder = gbv.ContourFinder(game_object=GAME_OBJECT, threshold_func=thr)
    distance = gbv.plane_distance_from_object(finder.locations_from_shapes(camera=CAMERA,
                                                                           shapes=finder.find_shapes(frame))[0])
    return abs(DISTANCE_FROM_OBJECT - distance)


def main():
    stream = gbv.TCPStreamReceiver(constants.net.TCP_STREAM_IP, constants.net.TCP_STREAM_PORT)
    ok, frame = stream.read()
    while not ok:
        pass

    functions = []
    for erode in range(10):
        for dilate in range(10):
            functions.append(((erode, dilate), calculate_distance(erode, dilate, frame)))
    best = None
    for function in functions:
        if best is None:
            best = function
        elif function[1] < best[1]:
            best = function

    print('Optimal Denoising: gbv.Erode(%f) + gbv.Dilate(%f)' % (best[0][0], best[0][1]))
