import gbvision as gbv

OUTER_PORT_THRESHOLD = gbv.ColorThreshold([[25, 105], [214, 255], [173, 253]], 'HSV') + gbv.MedianBlur(15)
POWER_CELL_THRESHOLD = gbv.ColorThreshold([[25, 45], [148, 228], [162, 242]], 'HSV') + gbv.Erode(3) + gbv.Dilate(5)
FEEDING_STATION_THRESHOLD = gbv.ColorThreshold([[25, 45], [148, 228], [162, 242]],'HSV')
