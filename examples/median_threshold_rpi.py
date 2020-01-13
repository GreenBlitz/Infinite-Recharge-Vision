import cv2
import numpy as np

import gbvision as gbv
from gbrpi.net.table_conn import TableConn

stdv = np.array([40, 40, 40])


def main():
    broadcast = gbv.TCPStreamBroadcaster(5808)
    stream_camera = gbv.USBStreamCamera(broadcast, 0)
    stream_camera.set_exposure(-3)
    stream_camera.toggle_stream(True)
    while True:
        stream_camera.read()

if __name__ == '__main__':
    main()
