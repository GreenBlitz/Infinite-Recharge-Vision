import gbvision as gbv

VISION_TARGET_THRESHOLD = gbv.ColorThreshold([[0, 50], [100, 255], [0, 50]], gbv.ColorThreshold.THRESH_TYPE_BGR)
OUTER_PORT_THRESHOLD = gbv.ColorThreshold([[25, 105], [215, 255], [189, 255]], 'HSV') + gbv.MedianBlur(3) + gbv.Dilate(2)
POWER_CELL_THRESHOLD = gbv.ColorThreshold([[25, 45], [148, 228], [162, 242]], 'HSV') + gbv.Erode(3) + gbv.Dilate(5)
