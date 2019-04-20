__author__ = 'Boris Polyanskiy'

import time
from threading import Thread

import RPi.GPIO as GPIO
import serial


RUN = True

ARDUINO_PIN = 12


def read_serial():
    raw_serial = ser.readline()
    value = int(raw_serial.decode().strip())
    return value


def read_serial_wrap():
    global RUN
    while RUN:
        value = read_serial()
        volts = value * 0.0049
        print('value: {}, volts: {:2.2f}, percents: {:2.2f}, status: {}'.format(
            value, volts, volts * 100 / 5, value > initial * 2))
        time.sleep(0.1)


def breath():
    values = []
    start_time = time.time()
    GPIO.output(ARDUINO_PIN, GPIO.HIGH)
    while time.time() < start_time + 5:
        values.append(read_serial())
        time.sleep(0.05)
    GPIO.output(ARDUINO_PIN, GPIO.LOW)
    return values


def interactive_run():
    global RUN
    t = Thread(target=read_serial_wrap)
    t.start()

    try:
        while True:
            input('wait')
            GPIO.output(ARDUINO_PIN, GPIO.HIGH)
            input('wait')
            GPIO.output(ARDUINO_PIN, GPIO.LOW)
    except KeyboardInterrupt:
        print('stop')
    RUN = False


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ARDUINO_PIN, GPIO.OUT)
    ser = serial.Serial('/dev/ttyUSB0', 115200)

    GPIO.output(ARDUINO_PIN, GPIO.HIGH)

    print('Read initial value...')
    values = []
    for _ in range(10):
        values.append(read_serial())
        time.sleep(0.05)
    initial = sum(values) / len(values)
    print('Initial value is {}'.format(initial))
    GPIO.output(ARDUINO_PIN, GPIO.LOW)

    input('Press "enter" when ready and breath to sensor')
    print('Breath now!')

    max_value = max(breath())
    print('Initial value: {}; breath maximum value is: {}'.format(initial, max_value))

    GPIO.cleanup(ARDUINO_PIN)
