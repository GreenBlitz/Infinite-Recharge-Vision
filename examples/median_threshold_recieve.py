import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([40, 40, 40])


def main():
    recieve = gbv.TCPStreamReceiver('192.168.1.8', 5808)
    window = gbv.StreamWindow('feed', recieve)
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()

    print(thr)

    threshold = gbv.StreamWindow('threshold', recieve, drawing_pipeline=thr)
    threshold.open()

    while True:
        ok, frame = recieve.get_frame()
        if not window.show_frame(frame):
            break
        if not threshold.show_frame(frame):
            break

    window.close()
    threshold.close()


if __name__ == '__main__':
    main()
