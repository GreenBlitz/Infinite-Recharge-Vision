import gbvision as gbv

VISION_TARGET_THRESHOLD = gbv.ColorThreshold([[0, 50], [100, 255], [0, 50]], gbv.ColorThreshold.THRESH_TYPE_BGR)
OUTER_PORT_THRESHOLD = gbv.ColorThreshold([[0, 167], [155, 255], [58, 138]], gbv.ColorThreshold.THRESH_TYPE_HSV) + gbv.MedianBlur(3) + gbv.Dilate(2)
POWER_CELL_THRESHOLD = gbv.ColorThreshold([[24, 34], [201, 255], [25, 125]], 'HSV') + gbv.Erode(5) + gbv.Dilate(5)