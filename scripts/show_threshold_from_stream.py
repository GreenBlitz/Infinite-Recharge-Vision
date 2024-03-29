import gbvision as gbv

from constants import TCP_STREAM_IP, TCP_STREAM_PORT

REMOTE_THRESHOLD = gbv.ColorThreshold([[63, 103], [7, 167], [157, 255]], 'HLS')


def main():
    receiver = gbv.AsyncTCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    receiver.wait_start_reading()
    window = gbv.StreamWindow(window_name='stream', wrap_object=receiver,
                              drawing_pipeline=gbv.DrawCircles(REMOTE_THRESHOLD, (0, 255, 0),
                                                               contours_process=gbv.FilterContours(100),
                                                               circle_process=gbv.sort_circles + gbv.filter_inner_circles,
                                                               thickness=5))
    window.show_async()
    threshold = gbv.StreamWindow(window_name='threshold', wrap_object=receiver, drawing_pipeline=REMOTE_THRESHOLD)
    threshold.show()


if __name__ == '__main__':
    main()
