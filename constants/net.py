from tools.system import is_on_roborio_network

__is_on_roborio_network = is_on_roborio_network()

TCP_STREAM_IP = '10.45.90.8' if __is_on_roborio_network else 'frcvision.local'
TCP_STREAM_PORT = 5809

STREAM_MAX_BITRATE = 5000
STREAM_USE_GRAYSCALE = True
STREAM_FX = 0.25
STREAM_FY = 0.25
