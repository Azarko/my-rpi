# !/usr/bin/env python3

__author__ = 'Boris Polyanskiy'

from time import sleep

import RPi.GPIO as GPIO

from myrpi.diode import RgbDiode


def diode_check():
    GPIO.setmode(GPIO.BCM)
    diode = RgbDiode(17, 27, 22)
    for color in diode.colors:
        color()
        sleep(0.5)
    diode.turn_off()
    del diode


if __name__ == '__main__':
    diode_check()
