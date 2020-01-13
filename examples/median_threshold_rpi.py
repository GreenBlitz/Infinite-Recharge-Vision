import cv2
import numpy as np

import gbvision as gbv
from gbrpi.net.table_conn import TableConn

stdv = np.array([40, 40, 40])


def main():
    broadcast = gbv.TCPStreamBroadcaster(5808, '192.168.1.60')
    camera = gbv.USBCamera(0)
    camera.set_exposure(-3)
    conn = TableConn('192.168.1.8', 'calibrate')
    conn.set('bbox', None)
    streaming = True
    while True:
        ok, frame = camera.read()
        if streaming:
            broadcast.send_frame(frame)
        k = conn.get('key')
        tr = conn.get('bbox')
        if k == 'r':
            streaming = False
        if tr is not None:
            thr = gbv.median_threshold(frame, stdv, tr, 'HSV')
            break

    conn.set('threshold', thr)

    while True:
        ok, frame = camera.read()
        broadcast.send_frame(frame)


if __name__ == '__main__':
    main()
