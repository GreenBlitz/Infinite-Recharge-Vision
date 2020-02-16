import gbvision as gbv
import cv2

from constants import TCP_STREAM_IP, TCP_STREAM_PORT

REMOTE_THRESHOLD = gbv.PipeLine(lambda x: cv2.GaussianBlur(x, (11, 11), cv2.BORDER_DEFAULT)) + gbv.ColorThreshold(
    [[19, 29], [0, 53], [215, 255]], 'HLS') + gbv.Erode(5) + gbv.Dilate(9) + gbv.MedianBlur(13)


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
