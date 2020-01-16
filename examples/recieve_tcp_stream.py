import gbvision as gbv

from constants import TCP_STREAM_IP, TCP_STREAM_PORT


def main():
    receiver = gbv.TCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    window = gbv.StreamWindow(window_name='stream example', wrap_object=receiver)
    window.show()


if __name__ == '__main__':
    main()
