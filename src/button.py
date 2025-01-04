from digitalio import DigitalInOut, Direction, Pull


class Button:
    def __init__(self, pin):
        self._pin = DigitalInOut(pin)
        self._pin.direction = Direction.INPUT
        self._pin.pull = Pull.UP

    def value(self):
        return not self._pin.value
