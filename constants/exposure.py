from tools.system import is_on_rpi

__is_on_rpi = is_on_rpi()

LOW_EXPOSURE = 10 if __is_on_rpi else -10
HIGH_EXPOSURE = 11 if __is_on_rpi else -3
