import cv2

import gbvision as gbv


def main():
    reciever = gbv.TCPStreamReceiver('192.168.1.8', 5808)
    window = gbv.StreamWindow('feed', reciever)
    window.open()
    conn = gbv.TableConn('calibrate')
    while True:
        frame = reciever.get_frame()
        k = window.last_key_pressed
        if k == 'r':
            conn.set('key', 'r')
            bbox = cv2.selectROI('feed', frame)
            break
    cv2.destroyAllWindows()

    print(conn.get('threshold'))


    original = gbv.StreamWindow('original', reciever)
    threshold = gbv.StreamWindow(window_name='threshold', drawing_pipeline=conn.get('threshold'), wrap_object=reciever)

    original.open()
    threshold.open()
    while True:
        frame = reciever.get_frame()
        if not original.show_frame(frame):
            break
        if not threshold.show_frame(frame):
            break

    original.close()
    threshold.close()


if __name__ == '__main__':
    main()
