import gbvision as gbv
from gbvision.gui.readable_window import ReadableWindow
import cv2

from constants import TCP_STREAM_IP, TCP_STREAM_PORT, OUTER_PORT

'''
this vision script was created to calibrate denoising of a threshod function for game objects
it finds the best constants for the erode and dilate denoising function in the bounds of 0 - 10
'''

# insert constants in the following variables:
THRESHOLD = gbv.ColorThreshold([[0, 65], [178, 255], [107, 187]], 'HSV')
# the threshold function used to detect the object
GAME_OBJECT = OUTER_PORT  # the game object object of the wanted game object
CAMERA = gbv.EmptyCamera(gbv.LIFECAM_3000, 640, 480)  # the camera used to detect the object
DISTANCE_FROM_OBJECT = 4.3


def calculate_distance(erode: int, dilate: int, frame: gbv.Frame, should_print=True):
    thr = THRESHOLD + gbv.Erode(erode) + gbv.Dilate(dilate)
    finder = gbv.ContourFinder(game_object=GAME_OBJECT, threshold_func=thr)
    distance = gbv.plane_distance_from_object(finder.locations_from_shapes(camera=CAMERA,
                                                                           shapes=finder.find_shapes(frame))[0]) if len(
        finder.find_shapes(frame)) > 0 else None

    if should_print and distance is not None:
        print(f"Erode: {erode}, Dilate: {dilate}, Distance: {distance}")
    return abs(DISTANCE_FROM_OBJECT - distance) if distance is not None else None


def main():
    #stream = gbv.TCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    stream = gbv.USBCamera(0, gbv.LIFECAM_3000)
    stream.set_exposure(-5)
    threshold = ReadableWindow('threshold', wrap_object=stream, drawing_pipeline=THRESHOLD)
    window = ReadableWindow(window_name='feed', wrap_object=stream,
                            drawing_pipeline=gbv.DrawContours(threshold_func=THRESHOLD, color=(0, 255, 0)))
    ok, frame = stream.read()
    while ok:
        ok, frame = stream.read()
        window.show_frame(frame)
        threshold.show_frame(frame)
        k = window.last_key_pressed
        if k == 'r' or k == 'R':
            break

    functions = []
    for erode in range(10):
        for dilate in range(10):
            erode_dilate = calculate_distance(erode, dilate, frame)
            dilate_erode = calculate_distance(dilate, erode, frame)
            functions.append(
                ((erode, dilate), erode_dilate, True)) if erode_dilate and erode_dilate == erode_dilate else None
            functions.append(
                ((erode, dilate), dilate_erode, False)) if dilate_erode and dilate_erode == dilate_erode else None
    best = None
    for function in functions:
        if best is None:
            best = function
        elif function[1] < best[1]:
            best = function

    print(
        f'Optimal Denoising: gbv.Erode({best[0][0] if best[2] else best[0][1]}) + gbv.Dilate({best[0][1] if best[2] else best[0][0]})' + 'Erode first' if
        best[2] else 'Dilate first')
    cv2.destroyAllWindows()

    original = ReadableWindow('original', wrap_object=stream)
    after_denoising = ReadableWindow('after denoising', wrap_object=stream,
                                     drawing_pipeline=THRESHOLD + gbv.Erode(best[0][0]) + gbv.Dilate(best[0][1]))
    while True:
        ok, frame = stream.read()
        after_denoising.show_frame(frame)
        original.show_frame(frame)
        print(str(calculate_distance(best[0][0], best[0][1], frame) + DISTANCE_FROM_OBJECT))


if __name__ == '__main__':
    main()
