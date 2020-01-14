import gbvision as gbv
import gbrpi as gbr


def main():
    broadcaster = gbv.TCPStreamBroadcaster(5809)
    camera = gbv.USBStreamCamera(broadcaster, 0, gbv.UNKNOWN_CAMERA)
    camera.set_exposure(50)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()
