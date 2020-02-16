import gbrpi as gbr
import gbvision as gbv
import numpy as np
import os
import cv2
import time

from constants.net import TCP_STREAM_IP, TCP_STREAM_PORT
from constants.network_tables import TABLE_IP, TABLE_NAME

seconds_left = 0
minutes_left = 0
start_time = 0

def update_time():
    global seconds_left, minutes_left, start_time
    if int(time.time()) - start_time > 0:
        if seconds_left == 0:
            seconds_left = 59
            minutes_left -= 1
        else:
            seconds_left -= 1



def draw(frame: gbv.Frame):
    global seconds_left, minutes_left, start_time
    update_time()
    timer_coord = 10, 9 * frame.shape[0] // 10
    time_left = f"0{minutes_left}:{seconds_left if seconds_left > 9 else f'0{seconds_left}'}"
    frame = gbv.draw_text(frame, color=(0, 0, 0), text=time_left, coords=timer_coord, font_scale=2, thickness=5)
    frame = gbv.draw_text(frame, color=(255, 255, 255), text=time_left, coords=timer_coord, font_scale=2, thickness=1)
    return frame


def on_game_state_change(new_state: str):
    global seconds_left, minutes_left, start_time
    if new_state == 'disabled':
        seconds_left = 00
        minutes_left = 00
    elif new_state == 'auto':
        seconds_left = 15
        minutes_left = 0
    elif new_state == 'teleop':
        seconds_left = 15
        minutes_left = 2
    start_time = int(time.time())

def main():
    # stream = gbv.TCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    stream = gbv.USBCamera(0)
    conn = gbr.TableConn(TABLE_IP, TABLE_NAME)
    conn.add_entry_change_listener(on_game_state_change, 'game_state')
    files = os.listdir('records/')

    last_index = max(map(lambda x: x[6:-4], files))
    window = gbv.RecordingCameraWindow('stream', stream, 'records/stream5.mp4', drawing_pipeline=draw)

    window.show()


if __name__ == '__main__':
    main()
