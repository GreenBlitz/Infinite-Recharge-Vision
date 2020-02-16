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
start_time = int(time.time())
conn = gbr.TableConn(TABLE_IP, TABLE_NAME)
shooter_conn = gbr.TableConn(TABLE_IP, 'Shooter')


def update_time():
    global seconds_left, minutes_left, start_time
    if int(time.time()) - int(start_time) != 0:
        start_time += 1
        print(f'start: {int(start_time)}\ncurrtime:{int(time.time())}\nsub: {int(time.time()) - int(start_time)}\n\n\n')
        if seconds_left == 0:
            seconds_left = 59
            minutes_left -= 1
        else:
            seconds_left -= 1


def draw(frame: gbv.Frame):
    global seconds_left, minutes_left, start_time, conn
    update_time()
    timer_coord = 10, 9 * frame.shape[0] // 10
    time_left = f"0{minutes_left}:{seconds_left if seconds_left > 9 else f'0{seconds_left}'}"
    frame = gbv.draw_text(frame, color=(0, 0, 0), text=time_left, coords=timer_coord, font_scale=2, thickness=5)
    frame = gbv.draw_text(frame, color=(255, 255, 255), text=time_left, coords=timer_coord, font_scale=2, thickness=1)

    gear = 'POWER' if conn.get('shifter_state') == 'power' else 'SPEED'
    gear_coord = 400, 9 * frame.shape[0] // 10
    frame = gbv.draw_text(frame, color=(0, 0, 0), text=gear, coords=gear_coord, font_scale=2, thickness=5)
    frame = gbv.draw_text(frame, color=(255, 255, 255), text=gear, coords=gear_coord, font_scale=2, thickness=1)

    found = conn.get('valid')
    found_coord = 20, 20
    color = (0, 255, 0) if found else (0, 0, 255)
    frame = gbv.draw_circles(frame, color=color, circs=[(found_coord, 10)], thickness=20)

    shooter_speed = str(int(shooter_conn.get('Velocity')))
    shooter_coord = 450, 50
    frame = gbv.draw_text(frame, color=(0, 0, 0), text=shooter_speed, coords=shooter_coord, font_scale=2, thickness=5)
    frame = gbv.draw_text(frame, color=(255, 255, 255), text=shooter_speed, coords=shooter_coord, font_scale=2, thickness=1)

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
    stream = gbv.AsyncTCPStreamReceiver(TCP_STREAM_IP, TCP_STREAM_PORT)
    #stream = gbv.USBCamera(0)
    conn.add_entry_change_listener(on_game_state_change, 'game_state')
    files = os.listdir('records/')
    if len(files) == 0:
        last_index = 0
    else:
        last_index = max(map(lambda x: x[6:-4], files))
    window = gbv.RecordingCameraWindow('stream', stream, 'records/stream5.mp4', drawing_pipeline=draw)

    window.show()


if __name__ == '__main__':
    main()
