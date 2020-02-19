from tools.system import is_on_rpi

__is_on_rpi = is_on_rpi()

STREAM_CAMERA_PORT = 0 if __is_on_rpi else 1
HEX_CAMERA_PORT = 1 if __is_on_rpi else 1
LED_RING_PORT = 18
