import gbvision as gbv
import cv2

from constants import TCP_STREAM_IP, TCP_STREAM_PORT

REMOTE_THRESHOLD = gbv.ColorThreshold([[0, 255], [100, 255], [0, 150]], 'BGR') + gbv.Dilate(4)


def main():
    receiver = gbv.AsyncTCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    receiver.wait_start_reading()
    window = gbv.StreamWindow(window_name='stream', wrap_object=receiver,
                              drawing_pipeline=gbv.DrawRects(REMOTE_THRESHOLD, (0, 255, 0),
                                                             contours_process=gbv.FilterContours(100),
                                                             # circle_process=gbv.sort_circles + gbv.filter_inner_circles,
                                                             thickness=5))
    window.show_async()
    threshold = gbv.StreamWindow(window_name='threshold', wrap_object=receiver, drawing_pipeline=REMOTE_THRESHOLD)
    threshold.show()


if __name__ == '__main__':
    main()
