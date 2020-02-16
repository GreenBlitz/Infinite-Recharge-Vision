import cv2
import gbvision as gbv

from constants import TCP_STREAM_PORT

THRESHOLD = gbv.ColorThreshold([[21, 31], [0, 50], [215, 255]], 'HLS')


def main():
    camera = gbv.AsyncTCPStreamReceiver('frcvision.local', TCP_STREAM_PORT)
    camera.wait_start_reading()

    draw_circles = gbv.DrawCircles(threshold_func=THRESHOLD + gbv.DistanceTransformThreshold(0.001), color=(0, 255, 0),
                                   thickness=5, contours_process=gbv.FilterContours(100))

    feed = gbv.CameraWindow('feed', camera, drawing_pipeline=draw_circles)
    regular_thresh = gbv.CameraWindow('threshold', camera, drawing_pipeline=THRESHOLD)
    blur_thresh = gbv.CameraWindow('blur', camera,
                                   drawing_pipeline=gbv.PipeLine(
                                       lambda x: cv2.GaussianBlur(x, (17, 17), cv2.BORDER_DEFAULT)) + draw_circles)
    blur_thresh.show_async()
    feed.show_async()

    regular_thresh.show()


if __name__ == '__main__':
    main()
