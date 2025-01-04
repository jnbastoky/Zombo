# The Display

We are starting with the display. I think this will be useful since it can provide some feedback without having to use the serial terminal.

## Summary

We plan on showing the following information on the display:

- Current State/Action
- Current Command
- Diagnostic Information

## Hardware

We are using the [Adafruit OLED Feather Wing][feather-wing-oled].  It's white a black and while 128x64 OLED display.  It communicates with the microcontroller via I2C.  There are 3 buttons on board the Feather Wing that we might use for something later.  

## Software

This display is supported by the Adafruit Circuit Python `adafruit_displayio_sh1107` library.  So we can easily write text to the display.

We are creating our own wrapper class to keep the main `code.py` cleaner.

```python
import board
import displayio
from adafruit_display_text import bitmap_label
import adafruit_displayio_sh1107
from i2cdisplaybus import I2CDisplayBus
import terminalio


displayio.release_displays()


class Display:
    def __init__(self, address=0x3C, i2c=board.I2C()):
        self._display_bus = I2CDisplayBus(i2c, device_address=address)

        # SH1107 is vertically oriented 64x128
        WIDTH = 128
        HEIGHT = 64

        self._display = adafruit_displayio_sh1107.SH1107(
            self._display_bus,
            width=WIDTH,
            height=HEIGHT
        )

        # Make the display context
        self._group = displayio.Group()
        self._display.root_group = self._group
```

We wil keep it simple for now and just include one method to add text to the display.  The `add_text()` method returns a reference to the text that was added so that it can be modified later if desired.

```python
    def add_text(self, text, x, y, color=0xFFFFFFFF, scale=1):
        # Draw some label text
        text_area = bitmap_label.Label(terminalio.FONT,
                                       text=text,
                                       color=color,
                                       x=x,
                                       y=y,
                                       scale=scale)
        self._group.append(text_area)
        return text_area

```

The display can also be put to sleep to save energy.  So we can expose those functionaly as well in the class.  It might come in handy later.

```python
    def sleep(self):
        print('Display is sleeping.')
        self._display.sleep()

    def wake(self):
        print('Display is waking.')
        self._display.wake()

    def is_awake(self):
        return self._display.is_awake
```

[feather-wing-oled]: https://www.adafruit.com/product/4650
