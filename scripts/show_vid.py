import gbvision as gbv
import cv2

THRESHOLD = gbv.ColorThreshold([[60, 100], [47, 207], [175, 255]], 'HLS') + gbv.Dilate(2)


def main(file):
    camera = gbv.USBCamera(file)
    window = gbv.FeedWindow(file, drawing_pipeline=THRESHOLD)
    thr = gbv.FeedWindow('raw')

    while True:
        ok, frame = camera.read()
        print(frame)
        window.show_frame(frame)
        thr.show_frame(frame)
    # window.show()


if __name__ == '__main__':
    main('record2.avi')
