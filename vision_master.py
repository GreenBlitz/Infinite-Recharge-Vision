from threading import Thread

import gbvision as gbv
import gbrpi

from algorithms import BaseAlgorithm, find_hexagon, find_feeding, find_power_cells
from constants import HEX_CAMERA_PORT, STREAM_CAMERA_PORT, TCP_STREAM_PORT, LED_RING_PORT, STREAM_PITCH_ANGLE, \
    STREAM_YAW_ANGLE, \
    STREAM_ROLL_ANGLE, STREAM_X_OFFSET, \
    STREAM_Y_OFFSET, STREAM_Z_OFFSET, HEX_PITCH_ANGLE, HEX_YAW_ANGLE, \
    HEX_ROLL_ANGLE, HEX_X_OFFSET, \
    HEX_Y_OFFSET, HEX_Z_OFFSET, STREAM_CAMERA_INDEX, STREAM_USE_GRAYSCALE, STREAM_MAX_BITRATE, STREAM_FX, STREAM_FY
from constants import TABLE_IP, TABLE_NAME, OUTPUT_KEY, SUCCESS_KEY
from tools.system import is_on_rpi
from utils.gblogger import GBLogger

LOGGER_NAME = 'vision_master'


class __EmptyLedRing:
    def __init__(self, port):
        pass

    def on(self):
        pass

    def off(self):
        pass


def cam_by_algo(algo):
    """
    :param algo: algorithm requiring camera
    :return: camera required for algorithm
    """
    return camera if algo == find_hexagon.FindHexagon else camera[1]


LedRing = gbrpi.LedRing if is_on_rpi() else __EmptyLedRing
camera = gbv.CameraList([])


def main():
    logger = GBLogger(LOGGER_NAME, use_file=True)
    logger.allow_debug = BaseAlgorithm.DEBUG
    conn = gbrpi.TableConn(ip=TABLE_IP, table_name=TABLE_NAME)
    led_ring = LedRing(LED_RING_PORT)
    logger.info('initialized conn')
    hex_data = gbv.LIFECAM_3000.rotate_pitch(HEX_PITCH_ANGLE). \
        rotate_yaw(HEX_YAW_ANGLE). \
        rotate_roll(HEX_ROLL_ANGLE). \
        move_x(HEX_X_OFFSET). \
        move_y(HEX_Y_OFFSET). \
        move_z(HEX_Z_OFFSET)

    stream_data = gbv.LIFECAM_3000.rotate_pitch(STREAM_PITCH_ANGLE). \
        rotate_yaw(STREAM_YAW_ANGLE). \
        rotate_roll(STREAM_ROLL_ANGLE). \
        move_x(STREAM_X_OFFSET). \
        move_y(STREAM_Y_OFFSET). \
        move_z(STREAM_Z_OFFSET)

    camera.add_camera(gbv.AsyncUSBCamera(STREAM_CAMERA_PORT, data=stream_data))
    camera.add_camera(gbv.USBCamera(HEX_CAMERA_PORT, data=hex_data))

    camera.select_camera(0)

    def __stream_thread():
        cam: gbv.AsyncCamera = camera[STREAM_CAMERA_INDEX]
        cam.wait_start_reading()
        streamer = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT, use_grayscale=STREAM_USE_GRAYSCALE,
                                            max_bitrate=STREAM_MAX_BITRATE, fx=STREAM_FX, fy=STREAM_FY)
        while True:
            _ok, _frame = cam.read()
            streamer.send_frame(_frame)

    Thread(target=__stream_thread).start()

    if BaseAlgorithm.DEBUG:
        logger.info('running on debug mode, waiting for a stream receiver to connect...')
        logger.info('initialized stream')

    camera.set_auto_exposure(False, foreach=True)
    # camera.rescale(0.5)
    logger.info('initialized camera')

    all_algos = BaseAlgorithm.get_algorithms()

    logger.debug(f'Algorithms: {", ".join(all_algos)}')

    possible_algos = {key: all_algos[key](OUTPUT_KEY, SUCCESS_KEY, conn) for key in all_algos}
    current_algo = None

    logger.info('starting...')

    while True:
        algo_type = conn.get('algorithm')
        if algo_type is not None:
            if algo_type not in possible_algos:
                logger.warning(f'Unknown algorithm type: {algo_type}')
                continue
            algo = possible_algos[algo_type]
            if algo_type != current_algo:
                logger.debug(f'switched to algorithm: {algo_type}')
                algo.reset(camera, led_ring)
            ok, frame = camera.read()
            if ok:
                algo(frame, camera)
            else:
                logger.warning(f'frame not read from camera during algorithm: {algo_type}')
        current_algo = algo_type


if __name__ == '__main__':
    main()
