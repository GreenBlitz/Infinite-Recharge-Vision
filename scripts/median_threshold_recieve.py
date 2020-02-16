import cv2
import numpy as np

import gbvision as gbv

from constants import TCP_STREAM_IP, TCP_STREAM_PORT

stdv = np.array([5, 20, 20])


def main():
    receive = gbv.TCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT, fx=1.5, fy=1.5)
    window = gbv.StreamWindow('feed', receive)
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, gbv.ColorThreshold.THRESH_TYPE_HLS)
            break
    cv2.destroyAllWindows()

    print(thr)

    threshold = gbv.StreamWindow('threshold', receive, drawing_pipeline=thr)
    threshold.open()

    while True:
        ok, frame = receive.read()
        if not window.show_frame(frame):
            break
        if not threshold.show_frame(frame):
            break

    window.close()
    threshold.close()


if __name__ == '__main__':
    main()
