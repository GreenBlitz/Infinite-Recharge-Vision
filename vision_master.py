from logging import Logger

import gbvision as gbv
import gbrpi
import numpy as np

from algorithms import BaseAlgorithm

TABLE_NAME = 'vision'
TABLE_IP = '10.45.90.2'
OUTPUT_KEY = 'output'
SUCCESS_KEY = 'found'
LOGGER_NAME = 'vision_master'


def main():
    logger = Logger(LOGGER_NAME)
    conn = gbrpi.TableConn(ip=TABLE_IP, table_name=TABLE_NAME)
    logger.debug('initialized conn')
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000.rotate_pitch(np.deg2rad(35)))
    logger.debug('initialized camera')

    all_algos = BaseAlgorithm.get_algorithms()

    possible_algos = {key: all_algos[key](OUTPUT_KEY, SUCCESS_KEY, conn) for key in all_algos}
    current_algo = None

    while True:
        ok, frame = camera.read()
        algo_type = conn.get('algorithm')
        if algo_type is not None:
            if algo_type != current_algo:
                possible_algos[algo_type].reset(camera)
            algo = possible_algos[algo_type]
            algo(frame, camera)
        current_algo = algo_type


if __name__ == '__main__':
    main()
