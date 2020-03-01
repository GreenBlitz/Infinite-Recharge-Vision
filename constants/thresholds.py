import gbvision as gbv

OUTER_PORT_THRESHOLD = gbv.ColorThreshold([[60, 100], [47, 207], [175, 255]], 'HLS') + gbv.Dilate(2)
POWER_CELL_THRESHOLD = gbv.ColorThreshold([[25, 45], [148, 228], [162, 242]], 'HSV') + gbv.DistanceTransformThreshold(0.6)
FEEDING_STATION_THRESHOLD = gbv.ColorThreshold([[25, 45], [148, 228], [162, 242]],'HSV')
