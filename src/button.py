from digitalio import DigitalInOut, Direction, Pull


class Button:
    def __init__(self, pin, pullup=True):
        self._pin = DigitalInOut(pin)
        self._pin.direction = Direction.INPUT
        if pullup:
            self._pin.pull = Pull.UP

    def value(self):
        return not self._pin.value
