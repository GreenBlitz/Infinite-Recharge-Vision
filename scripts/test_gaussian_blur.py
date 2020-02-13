import cv2
import gbvision as gbv

THRESHOLD = gbv.ColorThreshold([[0, 65], [178, 255], [107, 187]], 'HSV')


def main():
    camera = gbv.AsyncUSBCamera(0, gbv.LIFECAM_3000)
    camera.wait_start_reading(0.1)
    camera.set_exposure(-5)

    feed = gbv.CameraWindow('feed', camera)
    regular_thresh = gbv.CameraWindow('threshold', camera, drawing_pipeline=THRESHOLD)
    blur_thresh = gbv.CameraWindow('blur', camera,
                                   drawing_pipeline=gbv.PipeLine(
                                       lambda x: cv2.GaussianBlur(x, (17, 17), cv2.BORDER_DEFAULT)) + THRESHOLD)
    blur_thresh.show_async()
    feed.show_async()
    regular_thresh.show()


if __name__ == '__main__':
    main()
