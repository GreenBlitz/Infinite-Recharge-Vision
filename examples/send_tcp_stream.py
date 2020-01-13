import gbvision as gbv


def main():
    broadcaster = gbv.TCPStreamBroadcaster(5809)
    camera = gbv.USBStreamCamera(broadcaster, 0, gbv.UNKNOWN_CAMERA)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()