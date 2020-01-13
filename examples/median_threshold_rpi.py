import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([40, 40, 40])


def main():
    broadcast = gbv.TCPStreamBroadcaster(5808, '192.168.1.60')
    camera = gbv.USBCamera(0)
    camera.set_exposure(-3)
    conn = TableConn('threshold')
    conn.set('key', '')
    conn.set('threshold', None)
    streaming = True
    while True:
        ok, frame = camera.read()
        if streaming:
            broadcast.send_frame(frame)
        k = conn.get('key')
        tr = conn.get('threshold')
        if k == 'r':
            streaming = False
        if tr is not None:
            thr = gbv.median_threshold(frame, stdv, tr, 'HSV')
            break
    cv2.destroyAllWindows()

    print(thr)

    threshold = gbv.TCPStreamBroadcaster(5809)

    while True:
        ok, frame = camera.read()
        broadcast.send_frame(frame)
        thresholded = thr(frame)
        threshold.send_frame(thresholded)



if __name__ == '__main__':
    main()
