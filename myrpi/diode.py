from random import choice

import RPi.GPIO as GPIO


class RgbDiode(object):
    def __init__(self, r_pin, g_pin, b_pin):
        self.__r_pin = r_pin
        self.__g_pin = g_pin
        self.__b_pin = b_pin
        self.pins = (self.r_pin, self.g_pin, self.b_pin)
        if len(set(self.pins)) != 3:
            raise ValueError('Pins must be different!')
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.turn_off()

    # def __call__(self, *args, **kwargs):
    #     self.switch_random_color()

    def __del__(self):
        self.turn_off()
        GPIO.cleanup(self.pins)

    @property
    def colors(self):
        return self.red, self.green, self.blue, self.yellow, self.magenta, self.cyan, self.white

    def switch_random_color(self):
        choice(self.colors)()

    def get_current_color(self):
        color_bin = self.to_bin(*[GPIO.input(pin) for pin in self.pins])
        return color_bin

    @staticmethod
    def to_bin(*args):
        result = 0
        for counter, signal in enumerate(reversed(args)):
            result += signal * (2 ** counter)
        return bin(result)[1:]

    def turn_off(self):
        GPIO.output(self.pins, GPIO.LOW)

    def red(self):
        GPIO.output(self.r_pin, GPIO.HIGH)
        GPIO.output((self.g_pin, self.b_pin), GPIO.LOW)

    def green(self):
        GPIO.output(self.g_pin, GPIO.HIGH)
        GPIO.output((self.r_pin, self.b_pin), GPIO.LOW)

    def blue(self):
        GPIO.output(self.b_pin, GPIO.HIGH)
        GPIO.output((self.r_pin, self.g_pin), GPIO.LOW)

    def yellow(self):
        GPIO.output((self.r_pin, self.g_pin), GPIO.HIGH)
        GPIO.output(self.b_pin, GPIO.LOW)

    def magenta(self):
        GPIO.output((self.r_pin, self.b_pin), GPIO.HIGH)
        GPIO.output(self.g_pin, GPIO.LOW)

    def cyan(self):
        GPIO.output((self.g_pin, self.b_pin), GPIO.HIGH)
        GPIO.output(self.r_pin, GPIO.LOW)

    def white(self):
        GPIO.output(self.pins, GPIO.HIGH)

    @property
    def r_pin(self):
        return self.__r_pin

    @property
    def g_pin(self):
        return self.__g_pin

    @property
    def b_pin(self):
        return self.__b_pin


if __name__ == '__main__':
    from time import sleep, time
    GPIO.setmode(GPIO.BCM)
    diode = RgbDiode(17, 27, 22)
    for color in diode.colors:
        color()
        sleep(0.5)
    start_time = time()
    run_time = 120
    while start_time + run_time > time():
        try:
            diode.switch_random_color()
            sleep(0.5)
        except KeyboardInterrupt:
            break
    for color in reversed(diode.colors):
        color()
        sleep(0.5)
    diode.turn_off()
