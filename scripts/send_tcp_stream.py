import gbvision as gbv

from constants import TCP_STREAM_PORT, CAMERA_PORT, LOW_EXPOSURE, HIGH_EXPOSURE


def main():
    broadcaster = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
    camera = gbv.USBStreamCamera(broadcaster, CAMERA_PORT)
    camera.set_auto_exposure(False)
    camera.set_exposure(LOW_EXPOSURE)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()
