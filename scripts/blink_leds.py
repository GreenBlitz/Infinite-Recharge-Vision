import gbrpi
import time
import subprocess

LED_PORT = 18

BLINK_WAIT_TIME = 0.2
BLINKS_AMOUNT = 30


def main():
    led = gbrpi.LedRing(LED_PORT)

    while True:
        if subprocess.call(["ping", "-c", "5", "10.45.90.2"]) == 0:
            break
        time.sleep(0.1)

    for i in range(BLINKS_AMOUNT):
        led.on()
        time.sleep(BLINK_WAIT_TIME)
        led.off()
        time.sleep(BLINK_WAIT_TIME)

    while True:
        pass


if __name__ == '__main__':
    main()
