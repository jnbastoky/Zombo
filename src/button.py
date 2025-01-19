from digitalio import DigitalInOut, Direction, Pull


class Button:
    def __init__(self, pin, pullup=True):
        self._pin = DigitalInOut(pin)
        self._pin.direction = Direction.INPUT
        if pullup:
            self._pin.pull = Pull.UP
        self.last_value = self.value()

    def value(self):
        self.last_value = not self._pin.value
        return self.last_value

    def released(self):
        _last_value = self.last_value
        return not self.value() and _last_value
