import gbvision as gbv

from constants import TCP_STREAM_PORT, CAMERA_PORT


def main():
    broadcaster = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
    camera = gbv.USBStreamCamera(broadcaster, CAMERA_PORT)
    camera.set_exposure(0)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()
