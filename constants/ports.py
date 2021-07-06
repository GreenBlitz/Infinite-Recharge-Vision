from tools.system import is_on_rpi

__is_on_rpi = is_on_rpi()

HEX_CAMERA_PORT = 0 if __is_on_rpi else 1
STREAM_CAMERA_PORT = 11 if __is_on_rpi else 0
LED_RING_PORT = 18
