import board
import displayio
from adafruit_display_text import bitmap_label
import adafruit_displayio_sh1107
from i2cdisplaybus import I2CDisplayBus
import terminalio

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64

displayio.release_displays()


class Display:
    def __init__(self, address=0x3C, i2c=board.I2C()):
        self._display_bus = I2CDisplayBus(i2c, device_address=address)

        self._display = adafruit_displayio_sh1107.SH1107(
            self._display_bus,
            width=WIDTH,
            height=HEIGHT
        )

        # Make the display context
        self._group = displayio.Group()
        self._display.root_group = self._group

    def add_text(self, text, x, y, color=0xFFFFFF, scale=1):
        text_area = bitmap_label.Label(terminalio.FONT,
                                       text=text,
                                       color=color,
                                       x=x,
                                       y=y,
                                       scale=scale)
        self._group.append(text_area)
        return text_area

    def sleep(self):
        print('Display is sleeping.')
        self._display.sleep()

    def wake(self):
        print('Display is waking.')
        self._display.wake()

    def is_awake(self):
        return self._display.is_awake
